from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

TYPE_CHOICES = (
    ('C', 'Cliente'),
    ('F', 'Fornecedor'),
    ('A', 'Administrador'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    full_name = models.CharField(verbose_name='Nome completo', max_length=100)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C')
    discount = models.BooleanField(default=False)

    # Campos necessários para o AbstractBaseUser
    is_active = models.BooleanField(blank=True, null=True)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    # Adicione o related_name aqui para evitar o conflito
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.full_name or self.email
    
    @property
    def profile(self):
        for type in TYPE_CHOICES:
            if self.type == type[0]:
                return type[1]
            
    def status(self):
        status = {
            True: "Ativo",
            False: "Inativo",
            None: "Pendente"
        }

        return status[self.is_active]
