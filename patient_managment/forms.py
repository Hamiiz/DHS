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
        fields = ['doctor', 'appointment_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'placeholder': 'Add notes here',
                'rows': 4,
                'cols': 40,
            }),
            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
            }),}


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['notes', 'amount']
        widgets = {
            'notes': forms.Textarea(attrs={
                'placeholder': 'Add notes here',
                'rows': 4,
                'cols': 40,
            }),
            'amount': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        fixed_amount = kwargs.pop('fixed_amount', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        if fixed_amount is not None:
            self.fields['amount'].initial = fixed_amount