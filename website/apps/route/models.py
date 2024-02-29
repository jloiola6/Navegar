from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta, time

from apps.user.models import CustomUser as User
from apps.core.models import Utils

WEEKDAYS = (
    ('Sunday', 'Domingo'),
    ('Monday', 'Segunda-Feira'),
    ('Tuesday', 'Terça-Feira'),
    ('Wednesday', 'Quarta-Feira'),
    ('Thursday', 'Quinta-Feira'),
    ('Friday', 'Sexta-Feira'),
    ('Saturday', 'Sábado'),
)

class Boat(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=100)
    capacity = models.IntegerField(verbose_name="Capacidade", null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="Fornecedor", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Route(models.Model):
    origin = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='origin', verbose_name='Origem')
    destination = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='destination', verbose_name='Destino')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    discounted_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor com desconto (2,5%)', blank=True, null=True)
    cost_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Custo')
    discounted_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Custo com desconto (R$ 20,00)', blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True, verbose_name='Horário de partida')
    arrival_time = models.TimeField(blank=True, null=True, verbose_name='Horário de Horário')
    total_trip_time = models.CharField(max_length=10, blank=True, null=True, editable=False, verbose_name='Tempo total da viagem')
    after_midnight = models.BooleanField(default=False, verbose_name='Dia seguinte')

    def __str__(self):
        return f'{self.origin} - {self.destination}'
    
    def calculate_total_trip_time(self):
        # Crie objetos datetime apenas para as horas de partida e chegada
        start_datetime = datetime.combine(datetime.today(), self.departure_time)
        end_datetime = datetime.combine(datetime.today(), self.arrival_time)

        if self.after_midnight:
            end_datetime += timedelta(days=1)

        total_time = end_datetime - start_datetime

        # A lógica restante permanece inalterada
        total_seconds = total_time.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time = f"{int(hours):02}:{int(minutes):02}"

        return total_time
    
    def save(self, *args, **kwargs):
        if self.departure_time and  self.arrival_time:
            self.total_trip_time = self.calculate_total_trip_time()
        super(Route, self).save(*args, **kwargs)

    @property
    def get_value(self):
        if Utils.objects.all().exists():
            utils = Utils.objects.first()
        else:
            utils = Utils.objects.create()

        if utils.discount:
            return self.discounted_value
        return self.value
    
    class Meta:
        ordering = ['id']


class RouteWeekday(models.Model):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    weekday = models.CharField(choices=WEEKDAYS, max_length=15, verbose_name='Dia da semana')
    boat = models.ForeignKey(Boat, on_delete=models.PROTECT, verbose_name='Embarcação')
    

    def __str__(self):
        return f'{self.route} - {self.weekday}'
    
    @property
    def get_departure_time(self):
        return self.route.departure_time.strftime('%H:%M')
    
    @property
    def get_arrival_time(self):
        return self.route.arrival_time.strftime('%H:%M')
    
    @property
    def get_total_trip_time(self):
        return self.route.total_trip_time

