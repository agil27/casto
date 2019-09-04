from django.contrib.auth.models import AbstractUser
from django.db import models 

# Create your models here.
class User(AbstractUser):
    admin = models.BooleanField(default=False)

