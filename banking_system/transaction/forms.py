from django import forms
from .models import *

class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionModel
        fields = ['transaction_amount','transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
    
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.deposit
        return super().save()

class DepositForm(TransactionForm):
    def clean_transaction_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('transaction_amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'Deposit amount must be greater than {min_deposit_amount}'
            )    
        return amount

class WithdrawForm(TransactionForm):
    def clean_transaction_amount(self):
        min_withdraw_amount = 500
        max_withdraw_amount = 900000
        balance = self.account.deposit
        amount = self.cleaned_data.get('transaction_amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'Minimun withdarw amount is {min_withdraw_amount}'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'Maximum withdarw amount is {max_withdraw_amount}'
            )
        if amount > balance:
            raise forms.ValidationError(
                f'Not sufficient balance'
            )
        return amount 

class LoanForm(TransactionForm):
    def clean_transaction_amount(self):
        amount = self.cleaned_data.get('transaction_amount')
        return amount    

