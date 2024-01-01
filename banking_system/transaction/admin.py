from django.contrib import admin
from .models import *
from .views import send_transaction_mail
# Register your models here.
admin.site.register(Bank)
@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account','transaction_amount','balance_after_transaction','transaction_type','loan_approval']

    def save_model(self,request,obj,form,change):
        if obj.loan_approval == True:
            obj.account.deposit += obj.transaction_amount
            obj.balance_after_transaction = obj.account.deposit
            obj.account.save()
            send_transaction_mail(obj.account.user, obj.transaction_amount, 'Loan Approval', 'transactions/loan_approve.html')
        return super().save_model(request,obj,form,change)

