from django import forms
from django.db.models import fields
from django.forms import DateInput, NumberInput, PasswordInput, TextInput, widgets
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")

        return uname

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            user_group = Group.objects.get(name='client')

            user.groups.add(user_group)
        return user


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ["username", "password"]


class AddTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flight'].empty_label = 'Choose something'
    class Meta:
        model = Ticket
        fields = ['flight','seat']


class AddFlightForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Race'].empty_label = 'Choose race'
        self.fields['plane'].empty_label = 'Choose airship'
    class Meta:
        model = Flight
        fields = ['Race','startTime', 'plane']
        widgets = {
            'startTime': forms.DateInput(attrs={'type': 'datetime-local'}),
        }


class AddRaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['To'].empty_label = 'fly to'
        self.fields['RaceNumber'].widget = TextInput(attrs={'placeholder': 'Type number'})
        self.fields['Price'].widget = NumberInput(attrs={'placeholder': 'Price', 'step': '0.25'})
    class Meta:
        model = FlightRace
        fields = ['RaceNumber','From', 'To', 'Price']
        
        