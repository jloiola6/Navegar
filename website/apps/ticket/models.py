from django.db import models
from apps.user.models import CustomUser
from apps.route.models import RouteWeekday


STATUS_CHOICES = (
    (1, 'Pendente'),
    (2, 'Disponível'),
    (3, 'Cancelado'),
)

class Ticket(models.Model):
    user_create = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    route_weekday = models.ForeignKey(RouteWeekday, on_delete=models.PROTECT)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    boat = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    name_client = models.CharField(max_length=100, null=True, blank=True)
    docuemnt_client = models.CharField(max_length=11, null=True, blank=True)
    birth_date_client = models.DateField(null=True, blank=True)
    document = models.FileField("Anexar bilhete",upload_to='documents/', max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name_client} | ({self.origin} - {self.destination})'

    @property
    def get_document_url(self):
        if self.document:
            return f"{self.document.url}"
        return None
    
    @property
    def get_status(self):
        for choise in STATUS_CHOICES:
            if self.status == choise[0]:
                return choise[1]
            
    @property
    def is_upload(self):
        return self.route_weekday.boat.user.upload_ticket

    def update_status(self, status):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        if not self.value:
            self.origin = self.route_weekday.route.origin.name
            self.destination = self.route_weekday.route.destination.name
            self.boat = self.route_weekday.boat.name
            self.value = self.route_weekday.route.value
        
        if not self.pk and self.document:
            if Ticket.objects.filter(document__isnull=False).count() > 1000:
                Ticket.objects.filter(document__isnull=False).first().delete()
                
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
