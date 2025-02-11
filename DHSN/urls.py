
from django.contrib import admin
from django.urls import path,include
from patient_managment import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('su/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('admin/', views.admin_dashboard,name='admin_dashboard'),
    path('register/', views.register_patient, name='register_patient'),
    path('process_payment/<str:reason>/<int:patient_id>/', views.process_payment, name='process_payment'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.Logout, name='logout'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/payment/<str:txn_ref>/', views.view_payment, name='view_payment'),
    path('patient/<int:patient_id>/create_appointment/', views.create_appointment, name='create_appointment'),
    path('admin/scan/', views.scan_qr, name='scan_qr'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('payment_success/<str:reason>/<int:patient_id>/', views.payment_success, name='payment_success'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
