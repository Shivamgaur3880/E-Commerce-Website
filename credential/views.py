from django.shortcuts import render,redirect,HttpResponse
# from .models import cred
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import View
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def signup(request):

    if request.method == 'POST':
        email=request.POST['email']
        get_pass=request.POST['pass1']
        get_cpass=request.POST['pass2']

        if get_pass != get_cpass:
            messages.warning(request,"password is not matching")
            return render(request,'authentication/signup.html')
        
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email already exist")
                email_subject="Activate your Account"
                return redirect('/credential/login/')
            
        
        except Exception as identifier:
            pass

        user = User.objects.create_user(email,email,get_pass)
        user.is_active=False
        user.save()
        
        email_subject="Activate your Account"
        message = render_to_string('activate.html',{'user':user,
                                        'domain':'127.0.0.1:8000',
                                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token':generate_token.make_token(user)})
                                        
                                   

        send_mail(
    email_subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
        messages.success(request,f"Activation link send to your email.Activate your account{message}")
        return redirect('/credential/login/')
    return render(request,'authentication/signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/credential/login')
        return render(request,'activatefail.html')
        
    
        

# def verification(request):
    
#         return redirect('/credential/login')


def handlelogin(request):
    if request.method =="POST":
        email=request.POST['email']
        get_pass=request.POST['pass1']

        myuser=authenticate(username=email,password=get_pass)
       
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Successfully Login")
            return redirect('/')

        else:
            messages.success(request,"invalid email or passwaord")
            return redirect('/credential/login')

    return render(request,'authentication/login.html')

def handlelogout(request):

    logout(request)
    messages.info(request,'Logout Success')
    return redirect('/credential/login')