from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import FormView,UpdateView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def send_transaction_mail(user,receiver,amount,subject,template,email):
    message = render_to_string(template,{
        'user': user,
        'receiver': receiver,
        'amount': amount
    })
    send_mail = EmailMultiAlternatives(subject, '', to=[email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()

class Registration(FormView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)
    
class UserLogin(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogout(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
class EditProfile(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = EditForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
    
class TransferMoneyView(View):
    template_name = 'accounts/transfer_money.html'
    form_class = TransferForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            to_account_no = form.cleaned_data['to_account_no']
            amount = form.cleaned_data['amount']

            receiving_profile = get_object_or_404(UserAccount, account_no=to_account_no)

            if request.user.account.deposit >= amount:
                request.user.account.deposit -= amount
                receiving_profile.deposit += amount

                request.user.account.save()
                receiving_profile.save()

                messages.success(request, 'Transfer successful!')
                send_transaction_mail(request.user, receiving_profile.user, amount,'Transfer Money','accounts/transfer_mail.html',request.user.email )
                send_transaction_mail(request.user, receiving_profile.user, amount,'Received Money','accounts/receive_mail.html',receiving_profile.user.email )
                return redirect('home')
            else:
                messages.warning(request, 'Not enough balance for transfer.')
        return render(request, self.template_name, {'form': form})

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password changed')
            update_session_auth_hash(request,form.user)

            subject = 'Change of Password'
            message = render_to_string('accounts/pass_mail.html',{
            'user': request.user,
            })
            send_mail = EmailMultiAlternatives(subject, '', to=[request.user.email])
            send_mail.attach_alternative(message, 'text/html')
            send_mail.send()
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'accounts/pass_change.html',{'form':form})