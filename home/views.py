from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User  # use this for Creating User
from django.contrib.auth import authenticate, login, logout  # use this for login and logout the user 
from django.contrib import messages   #use this for Get message when signin,login go to singnup function..
from .models import UserProfile,Course,Category
from django.db.models import Count
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



# Create your views here.
def Home (request):
    return render(request, 'Home/home.html')

def ProfilePage(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    return render(request,'UserProfile/userprofile.html',{'userinfo':userinfo})

def updateProfile(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        picture = request.FILES.get("picture")
        username = request.POST.get("username")
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        birthdate = request.POST.get("birthdate")

        # Update the related User instance
        user = request.user
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update the UserProfile instance
        userinfo.phone = phone
        userinfo.address = address
        userinfo.birthdate = birthdate
        if picture:
            userinfo.picture = picture
        userinfo.save()
        messages.success(request, "Profile Updated Successfully!")
        return redirect("/profilePage/")
    return render(request, 'UserProfile/updateProfile.html', {'userinfo': userinfo})

def Products(request):
    courses = Course.objects.order_by('-studentOnCourse')[:6]
    category_counts = Category.objects.annotate(course_count=Count('course'))  
    context = {'courses':courses, 'categories':category_counts}
    return render(request, 'Products/productPage.html',context)

def AllCourses(request):
    if request.method == "GET":
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search)
        return render(request,"Products/allCourse.html",{'courses':course})
    courses = Course.objects.order_by('-studentOnCourse')
    context = {'courses':courses}
    return render(request,"Products/allCourse.html",context)

def ProductView(request,id):
    view =Course.objects.get(id=id)
    return render(request,'Products/productView.html',{'view':view})

@login_required
def CategoryCourses(request,id):
    try:
        category = Category.objects.get(id=id)
        courses = Course.objects.filter(courseCategory=category)
        context = {'courses': courses, 'category': category}
        return render(request, 'Products/categoryView.html', context)
    except Category.DoesNotExist:
        context = {'error_message': 'Category Courses not found.'}
        return render(request, 'Products/categoryView.html', context)


def About(request):
    return render(request,'About/about.html')

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
        referral_code = f"{user.first_name}@{user.email[2:10:2]}{random_numbers}"
        
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