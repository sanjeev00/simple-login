from django.shortcuts import render,redirect
from  .forms import RegForm ,OTPForm,FinalForm,Login
from .models import UserData,UserEncData
import bleach
from django.conf import settings
from django.core.mail import send_mail
from random import randint
import requests
from django.views.decorators.cache import cache_control

smsurl = "https://www.fast2sms.com/dev/bulk"

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.session.get('id') is not None:
        return redirect('profile')
    return render(request,'home/index.html',{'confirm': False})

def register(request):
    if request.method=='POST':
        form = RegForm(request.POST)
        if form.is_valid():
            print('valid')
            user = UserData()

            user.userId = bleach.clean(form.cleaned_data['name'])
            user.email = bleach.clean(form.cleaned_data['email'])
            user.phone = bleach.clean(form.cleaned_data['phone'])
            user.mailVerified = False
            user.phoneVerified = False
            old = UserData.objects.filter(email=user.email)
            ph = UserData.objects.filter(phone=user.phone,phoneVerified=True)
            if(len(ph)!=0):
                return render(request,'home/index.html',{'error':'phone number already in use','confirm':False})

            if(len(old)==0):
                user.save()
                old = [user]


            request.session['phone']= user.phone
            request.session['email']= old[0].email
            request.session['name'] = user.name

            request.session['mailVerified'] = old[0].mailVerified
            request.session['phoneVerified'] = old[0].phoneVerified
            if not old[0].mailVerified:
                otp = str( randint(100000,999999) )
                old[0].otp = otp
                old[0].save()

                sendEmail(otp,old[0].email)
                return redirect('email')
            elif not old[0].phoneVerified:
                otp = str(randint(100000, 999999))
                old[0].otp = otp
                old[0].phone = user.phone
                old[0].save()
                sendSMS(otp,old[0].phone)
                return redirect('phone')
            else:
                return redirect('confirm')

        return render(request,'home/index.html',{'error':form.errors,'confirm':False})
    else:
        return redirect('index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def email(request):
    email = request.session.get('email')
    mailVerified = request.session.get('mailVerified')
    if mailVerified is not None and mailVerified is True:

        return redirect('index')
    if email is not None:
        return render(request, 'home/email.html', {'email':email })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def phone(request):
    phone = request.session.get('phone')
    phoneVerified = request.session.get('phoneVerified')
    if phoneVerified is not None and phoneVerified is True:
        return redirect('index')
    if phone is not None:
        return render(request, 'home/mobile.html', {'phone': phone})

def sendEmail(otp,to):
    subject = 'OTP for your registration'
    message = 'Use this OTP to complete registration '+otp
    email_from = 'noreply@dashboard.reg'
    recipient_list = [to, ]

    send_mail(subject, message, email_from, recipient_list)

def sendSMS(otp,to):
    payload = "sender_id=FSTSMS&message=yourOTPis"+otp+"&language=english&route=p&numbers="+to
    headers = {
        'authorization': "bJvMqLDlE7zAu5arKismp2tFIeywkjNVdWQ13f8Bx0SnRhCT6XeNXvHGFRwkS6g9QnIa4yjUt8MrhlOV",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", smsurl, data=payload, headers=headers)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def confirmEmail(request):
    if request.session.get('id') is not None:
        return redirect('profile')
    if (request.session.get('mailVerified') is None) or request.session.get('mailVerified') is True:
        return redirect('index')
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if(form.is_valid()):
            email = request.session.get('email')
            if email is None:
                return redirect('index')
            user = UserData.objects.get(email=email)
            if user.otp==form.cleaned_data['otp']:
                user.mailVerified = True
                otp = str(randint(100000, 999999))
                user.otp = otp
                user.phone = request.session.get('phone',user.phone)
                user.save()
                sendSMS(otp, user.phone)
                request.session['mailVerified'] = True
                return redirect('phone')
            else:
                return render(request,'home/email.html',{'email':user.email,'error':'incorrect OTP'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def confirmPhone(request):
    if request.session.get('id') is not None:
        return redirect('profile')
    if (request.session.get('phoneVerified') is None) or request.session.get('phoneVerified') is True:
        return redirect('index')
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if(form.is_valid()):
            email = request.session.get('email')
            if email is None:
                return redirect('index')
            user = UserData.objects.get(email=email)
            if user.otp==form.cleaned_data['otp']:
                user.phoneVerified = True
                user.save()
                request.session['phoneVerified'] = True
                return redirect('confirm')
            else:
                return render(request,'home/mobile.html',{'phone':user.phone,'error':'incorrect OTP'})

def confirm(request):
    if request.session.get('id') is not None:
        return redirect('profile')
    if request.method == 'GET':

        email = request.session.get('email')
        if email is None:
            return redirect('index')
        user = UserData.objects.get(email=email)
        if user is not None:
            rid = str(user.id)
            try:
                enc = UserEncData.objects.get(userid=rid)
                return render(request, 'home/index.html', {'error': 'user already registered', 'confirm': False})
            except UserEncData.DoesNotExist:
                return render(request, 'home/index.html', {'confirm': True, 'user': user})

        else:
            return redirect('index')
    if request.method == 'POST':

        form = FinalForm(request.POST)
        if form.is_valid():
            user = UserEncData()
            user.email = request.session.get('email')
            user.phone = request.session.get('phone')
            user.name = form.cleaned_data['name']
            user.userid = str(UserData.objects.filter(email=user.email)[0].id)
            request.session['id'] = user.userid
            user.save()
            return redirect('profile')
        else:
            email = request.session.get('email')
            if email is None:
                return redirect('index')
            user = UserData.objects.get(email=email)
            if user is not None:
                return render(request, 'home/index.html', {'confirm': True, 'user': user})
            return render(request, 'home/index.html', {'confirm': True, 'user': user,'error':form.errors})


def profile(request):
    id =request.session.get('id')
    if id is None:
        return redirect('index')
    print(id)
    user = UserEncData.objects.get(userid=id)
    #print(user.getname())
    #print(user.getEmail())
    return render(request,'home/profile.html',{'email':user.getEmail(),'phone':user.getPhone(),'name':user.getname()})

def logout(request):
    if request.method=='POST':
        request.session.flush()
        return redirect('index')


def login(request):
    if request.session.get('id') is not None:
        return redirect('profile')
    if request.method =='POST':
        login = Login(request.POST)
        if login.is_valid():
            phone = login.cleaned_data['phone']
            user = UserData.objects.filter(phone=phone)
            if len(user)==0:
                return render(request, 'home/login.html', {'step': True,'error':'phone not registered'})
            if not user[0].phoneVerified:
                return render(request, 'home/login.html', {'step': True, 'error': 'phone not verified'})
            user = user[0]

            otp = str(randint(100000, 999999))
            request.session['login_phone'] = user.phone
            user.otp = otp
            user.save()
            sendSMS(otp, user.phone)
            return render(request,'home/login.html',{'step':False})
        else:
            return render(request, 'home/login.html', {'step': True,'error':login.errors})

    return render(request,'home/login.html',{'step':True})

def verifylogin(request):
    if request.session.get('id') is not None:
        return redirect('profile')
    if request.method =='POST':
        form = OTPForm(request.POST)
        if (form.is_valid()):
            phone= request.session.get('login_phone')
            if phone is None:
                return redirect('index')
            user = UserData.objects.get(phone=phone)
            if user.otp == form.cleaned_data['otp']:
                request.session['id'] = user.id
                user.save()
                return redirect('profile')
            else:
                return render(request, 'home/login.html', {'step': False, 'error': 'incorrect OTP'})
        else:
            return render(request, 'home/login.html', {'step': False, 'error': 'Invalid OTP'})