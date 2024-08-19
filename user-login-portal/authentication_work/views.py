from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from user_authentication import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
#force_text
from  .tokens import generate_token

# Create your views here.

def main(request):
    return render(request,'authentication_work/index.html')

def signup(request):

    if request.method == "POST":
        username= request.POST['username']
        first_name= request.POST['firstname']
        last_name= request.POST['lastname']
        email= request.POST['email']
        password= request.POST['password']
        password_confirmation= request.POST['confirm_password']

        if User.objects.filter(username=username):
            messages.error(request, "Username exists already, try some other username")
            return redirect('main')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email exists already, try some other email address")
            return redirect('main')

        if len(username) >10:
            messages.error(request, "Username's length should be less than or equal to 10")

        if password!=password_confirmation:
            messages.error(request, "Passwords donot match")
            
        if not username.isalnum():
            messages.error(request, "Username should be alpha numeric")
            return redirect('main')
        
        new_user= User.objects.create_user(username,email,password)
        new_user.first_name= first_name
        new_user.last_name= last_name
        new_user.is_active=False
        new_user.save()

        messages.success(request,"Account Created. Please activate your account by conforming your email address.")
        
        #Confomation Email

        subject = "Django User Authentication Portal"
        message = "Hello" + new_user.first_name + "!! \n" +"Welcome Django user authentication portal. Thanks for signing up. \n In order to activate your account please conform your email address \n\n Thankyou \n Django Account Activation."
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        #Email Address confirmation link
        current_site = get_current_site(request)
        email_subject = "Email Address Confirmation @ Django Sign_Up"
        message2 = render_to_string('email_confirmation.html',{
            'name': new_user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token': generate_token.make_token(new_user)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [new_user.email],
        )
        email.fail_silently =True
        email.send()

        return redirect('signin')

    return render(request,'authentication_work/signup.html')

def signin(request):
    if request.method=="POST":
        username= request.POST['username']
        password= request.POST['password']
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request, user)
            first_name=user.first_name
            return render(request, "authentication_work/index.html",{'firstname':first_name})
        else:
            messages.error(request, "No such Credentials Found")
            return redirect('main')
        
    return render(request,'authentication_work/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect('main')

def activate(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user=User.objects.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        return redirect('main')
    
    else:
        return redirect(request, 'activation_failed.html')
    
