from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Adicione quaisquer campos adicionais aqui para Cliente e Fornecedor
    pass

class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Adicione quaisquer campos adicionais aqui

class Fornecedor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Adicione quaisquer campos adicionais aqui