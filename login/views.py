from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from simplepostgres import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "login/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists, Try different username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Username already exists, Try different username")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
            
        if pass1==pass2:
            messages.error(request, "password is not matching")
            
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        
        myuser.save()
        
        messages.success(request, "Your account is created succesfully")
        
        #WELCOME EMAIL
        subject= "Welcome to page- django Login!"
        message = "Hello " + myuser.first_name + " !! \n" + "Welcome to Page \n Thank you for visiting our web page \n" + "Please confirm your mail ID \n\n" + "Thank you \n vinod sagar"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        print("email sent")
        
        return redirect('signin')
    
    return render(request, "login/signup.html")

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            firstname= user.first_name
            return render(request, "login/index.html", {'firstname': firstname})
        
        else:
            messages.error(request, "Bad creadentials!")
            return render(request, "login/signin.html")
    
    
    return render(request, "login/signin.html")

def signout(request):
    logout(request)
    messages.success(request, 'Logged out succesfully')
    return redirect('home')