from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Doctor, Appointment, Payment
from .forms import UserForm, AppointmentForm, PaymentForm
from .modules.chapa import chapa_payment_init, verify_payment
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
import datetime

def Logout(request):
    
    logout(request)
    return redirect('login')

def homepage(request):
    return render(request, 'homepage.html')

def register_patient(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name=form['name'].value(),
            phone_number=form['phone_number'].value()
            email=form['email'].value()
            username=form['username'].value()
            password=form['password'].value()
            user = User(
                name = name,
                email=email,
                username=username.lower(),
                password=password.strip(),
                phone_number=phone_number
            )
            
            user.set_password(str(password))
            user.save()
            current_user = User.objects.get(username=username)
            return redirect('patient_detail', patient_id=current_user.id)
    else:
        form = UserForm()
    return render(request, 'register_patient.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
       
            try:
                user = User.objects.get(username=username.lower())
                print(user)
                if check_password(password, user.password):
                    print('Password is correct')
                    login(request, user)
                    return redirect('patient_detail', patient_id=user.id)
                else:
            
                    return HttpResponse('Password is incorrect')
            except User.DoesNotExist:
                return HttpResponse('User does not exist')
    else:
    
        return render(request, 'user_login.html')
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})

def scan_qr(request):
    return render(request, 'qr_scanner.html')



@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'appointment_success.html')


def process_payment(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.patient = patient
            chapa_response = chapa_payment_init(payment.amount, patient)

            if chapa_response[0].status_code == 200:
                chapa_data = chapa_response[0].json()
                payment.transaction_id = chapa_response[1]
                print(payment.transaction_id)
                payment.payment_date = datetime.datetime.now()
                payment.save()
                return redirect(chapa_data['data']['checkout_url'])
            else:
                return render(request, 'process_payment.html', {'form': form, 'patient': patient, 'error': chapa_response[0].json()})
            
    else:
        form = PaymentForm()
    return render(request, 'process_payment.html', {'form': form, 'patient': patient})

def payment_success(request,patient_id):
    patient = get_object_or_404(User,id=patient_id)
    payment = Payment.objects.filter(patient=patient).first()
    txn_id = payment.transaction_id
    is_paid = verify_payment(txn_id)
    if is_paid.status_code ==200:
        payment.is_paid=True
        payment.save()
        return render(request, 'payment_success.html') 
    else:
        return redirect(f'http://127.0.0.1:8000/process_payment/{patient_id}/')
      
