from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.hashers import make_password

from user_auth.models.cpf import Cpf

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = email  # Set username as the provided email
        extra_fields.setdefault('username', username)
        extra_fields['password'] = make_password(password)  # Tokenize the password
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class BaseUser(AbstractUser):
    email = models.EmailField(_('endereço de e-mail'), unique=True)
    name = models.CharField (max_length=150, null=True, blank=True)
    cpf = models.OneToOneField(Cpf ,verbose_name="cpf", null=True, blank=True,
                             on_delete=models.CASCADE)
    password_confirmation = models.CharField(max_length=100, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        kwargs['using'] = 'default'
        self.username = self.email  # Set username as the email
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')