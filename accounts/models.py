from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        if not username:
            raise ValueError('The username field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Admin için gerekli
        extra_fields.setdefault('is_superuser', True)  # Admin için gerekli

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)  

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['email']  
    objects = CustomUserManager()

    def __str__(self):
        return self.username
