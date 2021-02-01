from Taxi.models import Driver, DriveRequest
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'Last Name'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control inputfield','placeholder':'password'})
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'Phone Number'}),
        }

class DriveRequestForm(forms.ModelForm):
    class Meta:
        model = DriveRequest
        fields = ('customer_name','customer_phone','traveller_count')

        widgets = {
            'customer_name': forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'Your Name'}),
            'customer_phone': forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'Phone Number'}),
            'traveller_count': forms.TextInput(attrs={'class':'form-control inputfield','placeholder':'Traveller Count'}),
        }
