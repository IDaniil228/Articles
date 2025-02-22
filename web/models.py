from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, null=False)
    surname = models.CharField(max_length=256, null=False)
    subscriptions = models.ManyToManyField('self', symmetrical=False, blank=True)
    photo = models.ImageField(upload_to="users/", null=True, blank = True)

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CustomUserManager()

    def __str__(self):
        return self.login



class Articles(models.Model):
    title = models.CharField(max_length=256, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="articles/", null=True, blank = True)


    def __str__(self):
        return self.title