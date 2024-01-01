from django.db import models
from account.models import UserAccount
from .constants import *
# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)
    is_bankrupt = models.BooleanField(default=False)

class TransactionModel(models.Model):
    account = models.ForeignKey(UserAccount, related_name = 'transaction', on_delete = models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=12, decimal_places = 2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places = 2)
    transaction_type = models.IntegerField(choices=TransactionType, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approval = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
