
from django.contrib import admin
from django.urls import path,include
from patient_managment import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('su/', admin.site.urls),
    path('register/', views.register_patient, name='register_patient'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.Logout, name='logout'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('scan/', views.scan_qr, name='scan_qr'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('process_payment/<int:patient_id>/', views.process_payment, name='process_payment'),
    path('payment_success/<int:patient_id>/', views.payment_success, name='payment_success'),
    path('', views.homepage, name='homepage'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
