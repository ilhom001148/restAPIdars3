from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=12,null=True,blank=True)
    address=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.username
