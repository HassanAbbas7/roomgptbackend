from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone



class Subscription(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    stripeId = models.CharField(max_length=40)
    priceId = models.CharField(max_length=40)
    nextInvoice = models.DateField()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=14)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    credits = models.IntegerField(default=3, max_length=40)
    date_joined = models.DateTimeField(auto_now_add=True) #auto_now = True if you want to add a field like "updated_on"
    USERNAME_FIELD = 'email'
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    REQUIRED_FIELDS = []
    objects = UserManager()


