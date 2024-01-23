from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta, time

from apps.user.models import CustomUser as User

WEEKDAYS = (
    ('Sunday', 'Domingo'),
    ('Monday', 'Segunda-Feira'),
    ('Tuesday', 'Terça-Feira'),
    ('wednesday', 'Quarta-Feira'),
    ('Thursday', 'Quinta-Feira'),
    ('Friday', 'Sexta-Feira'),
    ('Saturday', 'Sábado'),
)

class Boat(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Route(models.Model):
    origin = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='origin')
    destination = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='destination')
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.origin} - {self.destination}'
    
    class Meta:
        ordering = ['id']


class RouteWeekday(models.Model):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    weekday = models.CharField(choices=WEEKDAYS, max_length=15)
    boat = models.ForeignKey(Boat, on_delete=models.PROTECT)
    departure_time = models.TimeField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    total_trip_time = models.CharField(max_length=10, blank=True, null=True, editable=False)
    after_midnight = models.BooleanField('Dia seguinte', default=False)

    def __str__(self):
        return f'{self.route} - {self.weekday}'
    
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
    
    @property
    def get_departure_time(self):
        return self.departure_time.strftime('%H:%M')
    
    @property
    def get_arrival_time(self):
        return self.arrival_time.strftime('%H:%M')

    def save(self, *args, **kwargs):
        if self.departure_time and  self.arrival_time:
            self.total_trip_time = self.calculate_total_trip_time()
        super(RouteWeekday, self).save(*args, **kwargs)

