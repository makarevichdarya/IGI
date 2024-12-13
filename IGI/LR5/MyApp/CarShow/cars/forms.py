from django import forms
from datetime import date
import pytz

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, help_text='Username')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Password')


class RegistryForm(forms.Form):
    username = forms.CharField(max_length=30, help_text='Username')
    first_name = forms.CharField(max_length=30, help_text='Firstname')
    last_name = forms.CharField(max_length=30, help_text='Lastname')
    email = forms.EmailField(max_length=50, help_text='Email')
    phone_number = forms.CharField(max_length=30, help_text='Phone number', widget=forms.TextInput(attrs={
            'type': 'tel',
            'pattern': r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$', 
            'placeholder': '+375 (XX) XXX-XX-XX'}))
    birth = forms.DateField(help_text='Date of birth', widget=forms.DateInput(attrs={'type': 'date'}))
    time_zone = forms.ChoiceField( choices=[(tz, tz) for tz in pytz.common_timezones], initial='UTC')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Password')
    passwordConfirm = forms.CharField(widget=forms.PasswordInput(), help_text='Password confirm')

    def clean(self):
        cd = self.cleaned_data
        password1 = cd.get("password")
        password2 = cd.get("passwordConfirm")
        birth = cd.get("birth")
        today = date.today()
        age = (today.year - birth.year > 18) or ((today.year - birth.year == 18) and (today.month >= birth.month and today.day >= birth.day)) 
        if not age:
            raise forms.ValidationError("Age limit 18+")
        if password1 != password2:
            raise forms.ValidationError("Passwords did not match")

        return cd
    
