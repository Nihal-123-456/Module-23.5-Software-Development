from typing import Any
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .constants import *

class RegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=Account_Type)
    gender = forms.ChoiceField(choices=Gender)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=300)
    postal_code = forms.IntegerField()
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','account_type','gender','date_of_birth',
        'street_address','postal_code','city','country']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            date_of_birth = self.cleaned_data.get('date_of_birth')
            street_address = self.cleaned_data.get('street_address')
            postal_code = self.cleaned_data.get('postal_code')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')

            UserAccount.objects.create(
                user = user,
                account_type = account_type,
                gender = gender,
                date_of_birth = date_of_birth,
                account_no = 1000000+user.id,
            )

            UserAddress.objects.create(
                user = user,
                street_address = street_address,
                postal_code = postal_code,
                city = city,
                country = country,
            )
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

class EditForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=Account_Type)
    gender = forms.ChoiceField(choices=Gender)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=300)
    postal_code = forms.IntegerField()
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserAccount.DoesNotExist:
                user_account = None
                user_address = None
            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['date_of_birth'].initial = user_account.date_of_birth
                self.fields['street_address'].initial = user_address.street_address
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['city'].initial = user_address.city
                self.fields['country'].initial = user_address.country
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            user_account,created = UserAccount.objects.get_or_create(user=user)
            user_address,created = UserAddress.objects.get_or_create(user=user)

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.date_of_birth = self.cleaned_data['date_of_birth']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.city = self.cleaned_data['city']
            user_address.country = self.cleaned_data['country'] 
            user_address.save()
        
        return user

class TransferForm(forms.Form):
    to_account_no = forms.CharField()
    amount = forms.DecimalField()
        
            
            
