from django.db import models
from apps.user.models import CustomUser
from apps.route.models import RouteWeekday


STATUS_CHOICES = (
    (1, 'Pendente'),
    (2, 'Aprovado'),
    (3, 'Cancelado'),
)

class Ticket(models.Model):
    user_create = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    route_weekday = models.ForeignKey(RouteWeekday, on_delete=models.PROTECT) # Tabela intermediaria rota / barco

    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    boat = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    name_client = models.CharField(max_length=100, null=True, blank=True)
    docuemnt_client = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return f'{self.name_client} | ({self.origin} - {self.destination})'
    
    def update_status(self, status):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        if not self.value:
            self.origin = self.route_weekday.route.origin.name
            self.destination = self.route_weekday.route.destination.name
            self.boat = self.route_weekday.boat.name
            self.value = self.route_weekday.route.value
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']