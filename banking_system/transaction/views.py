from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from .forms import *
from .constants import *
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.views import View
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
# Create your views here.
def send_transaction_mail(user,amount,subject,template):
    message = render_to_string(template,{
        'user': user,
        'amount': amount
    })
    send_mail = EmailMultiAlternatives(subject, '', to=[user.email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()

class TransactionMixin(LoginRequiredMixin,CreateView):
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    title = ''
    model = TransactionModel

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context
    
class DepositView(TransactionMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type':DEPOSIT}
        return initial
    def form_valid(self, form):
        account = self.request.user.account
        amount = form.cleaned_data['transaction_amount']
        account.deposit += amount
        account.save(
            update_fields = ['deposit']
        )
        messages.success(self.request, f'{amount} tk successfully deposited')

        send_transaction_mail(self.request.user, amount, 'Deposit email', 'transactions/deposit_mail.html')
        return super().form_valid(form)
    
class WithdrawView(TransactionMixin):
    form_class = WithdrawForm
    title = 'Withdraw'

    def get_initial(self):
        initial = {'transaction_type':WITHDRAW}
        return initial
    def form_valid(self, form):
        if Bank.objects.get(name='Mamar Bank').is_bankrupt is False:
            account = self.request.user.account
            amount = form.cleaned_data['transaction_amount']
            account.deposit -= amount
            account.save(
                update_fields = ['deposit']
            )
            messages.success(self.request, f'{amount} tk successfully withdrawn')
            
            send_transaction_mail(self.request.user, amount, 'Withdraw email', 'transactions/withdraw_mail.html')
            return super().form_valid(form)
        else:
            messages.warning(self.request, f'Bank is Bankrupt')
            return redirect('withdraw')
    
class LoanRecieveView(TransactionMixin):
    form_class = LoanForm
    title = 'Loan Recieve'

    def get_initial(self):
        initial = {'transaction_type':RECIEVE_LOAN}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data['transaction_amount']
        loan_count = TransactionModel.objects.filter(account=self.request.user.account, transaction_type=3,
        loan_approval=True).count()
        if loan_count>=3:
            return HttpResponse('Loan limit exceeded')
        
        messages.success(self.request, f'{amount} tk successfully applied for loan')
        send_transaction_mail(self.request.user, amount, 'Loan Request email', 'transactions/loan_mail.html')
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    deposit = 0
    model = TransactionModel

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date)

            self.deposit = TransactionModel.objects.filter(timestamp__date__gte = start_date,
            timestamp__date__lte = end_date).aggregate(Sum('transaction_amount'))['transaction_amount__sum']
        else:
            self.deposit = self.request.user.account.deposit
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        return context
    
class LoanPayView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(TransactionModel, id=loan_id)
        if loan.loan_approval:
            user_account = loan.account
            amount = loan.transaction_amount
            if user_account.deposit > amount:
                user_account.deposit -= amount
                loan.balance_after_transaction = user_account.deposit
                loan.transaction_type = PAY_LOAN
                loan.save()
                user_account.save()
                return redirect('loan_list')
            else:
                messages.warning(self.request, 'Not enough balance for paying the loan')
                return redirect('loan_list')

class LoanListView(LoginRequiredMixin, ListView):
    template_name = 'transactions/loan_list.html'
    model = TransactionModel
    context_object_name = 'loans'

    def get_queryset(self):
        queryset = TransactionModel.objects.filter(account=self.request.user.account, transaction_type=3)
        return queryset



