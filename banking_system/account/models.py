from django.db import models
from django.contrib.auth.models import User
from .constants import *
# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=Account_Type)
    account_no = models.IntegerField(unique=True)
    gender = models.CharField(max_length=20, choices=Gender)
    date_of_birth = models.DateField(null=True, blank=True)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    initial_deposit_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.account_no)

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=300)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email
