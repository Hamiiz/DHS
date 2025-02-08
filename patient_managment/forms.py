from django import forms
from .models import User,Appointment, Payment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone_number', 'email',  'password']
        widgets = {
            'password': forms.PasswordInput(),
        }




class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient','doctor', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']