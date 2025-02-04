from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length= 256, unique = True)
    name = models.CharField(max_length= 256, null=False)
    surname = models.CharField(max_length= 256, null=False)
    subscriptions = models.ManyToManyField(settings.AUTH_USER_MODEL);


class Articles(models.Model):
    title = models.CharField(max_length=256, null=False)
    create_date = models.DateField(null=False)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE());