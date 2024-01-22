from django.db import models
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
