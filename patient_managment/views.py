import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import User, Doctor, Appointment, Payment
from .forms import UserForm, AppointmentForm, PaymentForm
from .modules.chapa import chapa_payment_init, verify_payment
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

def is_staff_user(user):
    return user.is_staff

def Logout(request):
    
    logout(request)
    return redirect('login_user')

def homepage(request):
    return render(request, 'homepage.html')

def register_patient(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
       
            name=form['name'].value()
            phone_number=form['phone_number'].value()
            email=form['email'].value()
            username=form['username'].value()
            password=form['password'].value()
            user = User(
                name = name,
                email=email,
                username=username.lower().strip(),
                password=password.strip(),
                phone_number=phone_number
            )
            
            user.set_password(str(password))
      
            user.save()
        
            current_user = User.objects.get(username=str(username).lower().strip())
            login(request, current_user)
         
            return redirect('process_payment', patient_id=int(current_user.id),reason = 'cardfee')
    else:
        form = UserForm()
        return render(request, 'register_patient.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
       
            try:
                user = User.objects.get(username=username.lower())
         
                if check_password(password, user.password):
           
                    login(request, user)
                    if user.is_staff:
                        return redirect('admin_dashboard')
                    payment = user.payments.get(patient=user.id,amount=200)
                    if payment.is_paid == True:
                        return redirect('patient_detail', patient_id=user.id)
                    else:
                        return redirect('process_payment', patient_id=user.id,reason='cardfee')
                    
                else:
            
                    return render(request, 'user_login.html',{'error':'incorect password'})
            except User.DoesNotExist:
                return render(request, 'user_login.html',{'error':'No username like that'})
    else:
    
        return render(request, 'user_login.html')
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    payments= patient.payments.all()
    appointments = patient.appointments.all()
    payment_amounts = []
    for i in payments:
        payment_amounts.append(i.amount)
    if 200 in payment_amounts:
       return render(request, 'patient_detail.html', {'patient': patient,'payments':payments,'appointments':appointments,'patient_id':patient_id})
    else:
        return redirect('process_payment', patient_id=patient_id,reason='cardfee')
@login_required
@user_passes_test(is_staff_user)
def scan_qr(request):
    return render(request, 'qr_scanner.html')

@login_required
def create_appointment(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        # doctor = get_object_or_404(Doctor,name=form['doctor'])
        if form.is_valid():
            doctor = get_object_or_404(Doctor, id=form.cleaned_data['doctor'].id)
            appointment = Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=form.cleaned_data['appointment_date'],
            notes=form.cleaned_data['notes'],
            
            )
            appointment.save()
            doctor.count +=1
    
            print('about to take off')
            return redirect('process_payment', patient_id=patient_id, reason='appointmentfee')

           
        
    else:
        form = AppointmentForm()
        return render(request, 'create_appointment.html', {'form': form, 'patient': patient})

def appointment_success(request):
    return render(request, 'appointment_success.html')

@login_required
def process_payment(request, patient_id,reason):
    patient = get_object_or_404(User, id=patient_id)
    payments = patient.payments.all()
    fixed_amount = None
    if reason == 'cardfee':
            fixed_amount = 200
    else:
            fixed_amount = 150
    print('requesting GET')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, fixed_amount=fixed_amount)
        # this is for payment initialization
        if form.is_valid():

            payment = form.save(commit=False)
            payment.patient = patient
            payment.amount = fixed_amount
            base_url = request.build_absolute_uri('/')
            chapa_response = chapa_payment_init(fixed_amount, patient,reason,base_url)

            if chapa_response[0].status_code == 200:
                chapa_data = chapa_response[0].json()
                payment.transaction_id = chapa_response[1]
                payment.payment_date = datetime.datetime.now()
                payment.save()
                return redirect(chapa_data['data']['checkout_url'])
            else:
           
                return render(request, 'process_payment.html', {'form': form, 'patient': patient,'amount':fixed_amount,'error': chapa_response[0].json()})
            
        else:
            print(form.errors)
            return render(request, 'process_payment.html', {'form': form, 'patient': patient,'amount':fixed_amount})  
    else: 
        pay = False 
        print('forloop abouta start')
        if len(payments)==0:
                    pay=True
        else:
            for p in payments:
                print('forloop startedt')

                if reason == 'cardfee':
                    print('reason checked')
                    
                    if p.amount == 200:
                        pay = False
                        print('200 payment found')
                        break
                    
                    else:
                        print('not 200')
                        pay = True
                else:
                    pay=True
                   
        if pay:
            form = PaymentForm(fixed_amount=int(fixed_amount))
            return render(request, 'process_payment.html', {'form': form, 'patient': patient,'amount':fixed_amount})
        else:
            return redirect(f'/patient/{patient_id}')
         
@login_required
def payment_success(request,patient_id,reason):
    patient = get_object_or_404(User,id=patient_id)
    if reason == 'cardfee':
        payment = patient.payments.get(patient=patient_id,amount=200)
        txn_id = payment.transaction_id

        is_paid = verify_payment(txn_id)
        if is_paid.status_code ==200:
            payment.is_paid=True
            payment.save()
            return redirect('patient_detail', patient_id=patient_id)
        else:
            return redirect('process_payment',patient_id=patient_id,reason='cardfee')
    else:
        payment = patient.payments.filter(patient=patient_id,amount=
        150).order_by('-payment_date').first()
       
        appointment = patient.appointments.filter(patient=patient_id).order_by('-id').first()
        txn_id = payment.transaction_id

        is_paid = verify_payment(txn_id)
        print(is_paid)
        if is_paid.status_code ==200:
            appointment.payment_status=True
            appointment.save()
            return redirect('patient_detail', patient_id=patient_id)
        else:
            return redirect('process_payment',patient_id=patient_id,reason='appointmentfee')
       
@login_required
def view_payment(request,txn_ref,patient_id):
    verifyer = verify_payment(txn_ref)
    patient = get_object_or_404(User,id=patient_id)
    payment = patient.payments.get(patient=patient_id,transaction_id=txn_ref)
    stat = verifyer.status_code
    if stat == 200:
        
        details = {
            'name' : patient.name,
            'date': payment.payment_date,
            'amount': payment.amount,
            'email': patient.email,
            'txn':txn_ref

        }
   

    return render(request, 'view_payment.html', {'payer': details,'patient_id':patient_id})




@login_required
def admin_dashboard(request):
    appointments = Appointment.objects.all()
    payments = Payment.objects.all()
    doctors = Doctor.objects.all()

    
    most_visited_doctor = doctors.order_by('-count').first()
    payment_trends = payments.values('payment_date').order_by('payment_date')
    

    context = {
        'appointments': appointments,
        'payments': payments,
        'doctors': doctors,
        'most_visited_doctor': most_visited_doctor,
        'payment_trends': list(payment_trends)
    }
    return render(request, 'admin_dash.html', context)
