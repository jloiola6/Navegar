from django.db import models
from apps.user.models import CustomUser


STATUS_CHOICES = (
    (1, 'Pendente'),
    (2, 'Aprovado'),
    (3, 'Cancelado'),
)

class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    boat = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.name + ' - ' + self.cpf + ' (' + self.origin + ' - ' + self.destination + ')'
    
    def update_status(self, status):
        self.status = status
        self.save()
    
    class Meta:
        ordering = ['id']