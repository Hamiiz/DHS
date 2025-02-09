from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.contrib.auth.hashers import make_password
import os
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    username = models.CharField(max_length=100,unique=True,null=True)
    password = models.CharField(max_length=128, null=True)
  
    def __str__(self):
        return self.username
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:  # Generate QR code if it doesn't exist
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5,
            )
            qr.add_data(f"User ID: {self.id}")
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            filename = f'qr_code_{self.id}.png'
            self.qr_code.save(filename, File(buffer), save=False)
        super().save(*args, **kwargs)

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')],default='Pending')
    payment_status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"

class Payment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cardfee_is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.amount}"
