from django.contrib import admin
from .models import User, Doctor, Appointment, Payment

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Payment)
