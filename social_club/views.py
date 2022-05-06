import email
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User
from django.db import IntegrityError

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST["name"]
        email_address= request.POST["email_address"]
        send_mail(
            "Hi",
             f"{name} says Hi",
            email_address,
            ['mukeshkp2005@gmail.com'],
            fail_silently=False, 
        )
    return render(request,'social_club/hello.html')
    
def about(request):
    return render(request, 'social_club/about.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "social_club/hello.html")
        else:
            return render(request, "social_club/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "social_club/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, phone=phone)
            user.save()
        except IntegrityError:
            return render(request, "social_club/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "social_club/hello.html")
    else:
        return render(request, "social_club/register.html")