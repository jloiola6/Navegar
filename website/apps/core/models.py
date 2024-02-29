from django.db import models

# Create your models here.

class Utils(models.Model):
    discount = models.BooleanField(default=False)
