from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    # Adicione quaisquer campos adicionais aqui
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Fornecedor(models.Model):
    # Adicione quaisquer campos adicionais aqui
    user = models.OneToOneField(User, on_delete=models.CASCADE)