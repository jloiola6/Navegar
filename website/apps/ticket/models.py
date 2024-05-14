from django.db import models
import uuid
from django.utils import timezone

from apps.user.models import CustomUser
from apps.route.models import RouteWeekday


STATUS_CHOICES = (
    (1, 'Pendente'),
    (2, 'Cancelado pelo solicitante'),
    (3, 'Recusado pelo fornecedor'),
    (4, 'Disponível'),
    (5, 'Cancelado pelo fornecedor'),
    (6, 'Finalizado'),
    (7, 'Não comparecimento'),
)

STATUS_CLASSES = (
    (1, 'pending'),
    (2, 'order_cancellation'),
    (3, 'refused'),
    (4, 'available'),
    (5, 'canceled'),
    (6, 'finished'),
    (7, 'no_show'),
)

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    user_create = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    route_weekday = models.ForeignKey(RouteWeekday, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, default='passenger')
    
    # ROUTE DATA
    created_at = models.DateTimeField(auto_now_add= True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    boat = models.CharField(max_length=100)

    # FINANCIAL DATA
    value = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits= 10, decimal_places= 2)

    # CLIENT DATA
    name_client = models.CharField(max_length=100, null=True, blank=True)
    document_client = models.CharField(max_length=11, null=True, blank=True)
    document_type = models.CharField(max_length=3, null=True)
    birth_date_client = models.DateField(null=True, blank=True)

    # CARGO DATA
    cargo_description = models.CharField(max_length=100, null= True)
    cargo_weight = models.CharField(max_length=10, null= True)

    # STATUS DATA
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    document = models.FileField("Anexar bilhete",upload_to='documents/', max_length=100, blank=True, null=True)
    markdown = models.BooleanField(default= False)

    def __str__(self):
        return f'{self.name_client} | ({self.origin} - {self.destination})'
    
    @property
    def get_document_client(self):
        return self.document_client or 'N/A'
    
    @property
    def get_birth_date_client(self):
        return self.birth_date_client or 'N/A'
    
    @property
    def get_cargo_weight(self):
        return self.cargo_weight or 'N/A'

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
    def get_status_class(self):
        for css_class in STATUS_CLASSES:
            if self.status == css_class[0]:
                return css_class[1]
            
    @property
    def is_upload(self):
        return self.route_weekday.boat.supplier.upload_ticket
    
    @property
    def profit(self):
        return self.value - self.cost
    
    @property
    def supplier(self):
        return self.route_weekday.boat.supplier

    def update_status(self, status):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk and self.document:
            if Ticket.objects.filter(document__isnull=False).count() > 1000:
                Ticket.objects.filter(document__isnull=False).first().delete()
                
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
