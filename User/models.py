
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default="user")
    status = models.CharField(max_length=20, default="user")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    

    def __str__(self):
        return self.email
