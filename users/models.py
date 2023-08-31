# Create your models here.

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Utente(AbstractUser):
    """Base user that can register only with email and password"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField('email', unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    acceptance = models.BooleanField(verbose_name=_("Accettazione privacy"), default=False, blank=False, null=False)
    newsletter = models.BooleanField(verbose_name=_("Accettazione newsletter"), default=False, blank=True, null=False)
    date_acceptance = models.DateTimeField(default=timezone.now)
    date_newsletter = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('detailUtente', args=[str(self.pk)])

    def __str__(self):
        return self.username + " " + self.email
