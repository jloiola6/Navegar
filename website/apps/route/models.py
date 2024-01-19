from django.db import models

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

    def __str__(self):
        return self.name

class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    weekday = models.CharField(choices=WEEKDAYS, max_length=15)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.origin + ' - ' + self.destination + ' (' + self.weekday + ')'
    
    class Meta:
        ordering = ['id']