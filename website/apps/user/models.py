from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    # Adicione quaisquer campos adicionais aqui

class Fornecedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fornecedor')
    # Adicione quaisquer campos adicionais aqui