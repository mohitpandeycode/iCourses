from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User  # use this for Creating User
from django.contrib.auth import authenticate, login, logout  # use this for login and logout the user 
from django.contrib import messages   #use this for Get message when signin,login go to singnup function..
from .models import UserProfile
import random
import string


# Create your views here.
def Home (request):
    return render(request, 'Home/home.html')

def ProfilePage(request):
    return render(request,'UserProfile/userprofile.html')


def UserSignup(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')

        # Validate username length
        if len(username) < 3:
            messages.error(request, "Invalid Username")
            return redirect("/signup/")

        # Check password and confirm password match
        if password != cpassword:
            messages.error(request, "Password and Confirm Password do not match! ")
            return redirect("/signup/")
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Already taken!")
            return redirect("/signup/")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already exists, try to login!")
            return redirect("/signup/")
    
        # Create user
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Generate random referral code for every user
        random_numbers = ''.join(random.choices('0123456789', k=3))
        referral_code = f"{user.first_name}@{user.email[3:10:2]}{random_numbers}"
        
        # Assign random referral code to UserProfile of user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.referral_link = referral_code
        user_profile.save()

        messages.success(request, "Account Created Successfully!")
        return redirect("/login/")

    return render(request, "login-signup/signup.html")


def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password') 
        # Check the username (email) exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username!')
            return redirect("/login/")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Login the user
        if user is None:
            messages.error(request, 'Invalid Password!')
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/")

    return render(request, "login-signup/login.html")

def UserLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    return HttpResponse('<h1>Error 404 - Page not found!</h1>')