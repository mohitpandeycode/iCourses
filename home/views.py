from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User  # use this for Creating User
from django.contrib.auth import authenticate, login, logout  # use this for login and logout the user 
from django.contrib import messages   #use this for Get message when signin,login go to singnup function..
from .models import UserProfile,Course,Category,OrdersPayment,Event,EventRegistration,Sales
from django.db.models import Count
import random
import razorpay
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest,HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.db.models import Sum
import threading


# Create your views here.
# making email thread to send without loading******************************
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# Home page view***********************************************************
def Home (request):
    if request.method == "GET": #search functionality.....
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search)
        return render(request,"Products/allCourse.html",{'courses':course})
    return render(request, 'Home/home.html')

# Profile page view********************************************************
def ProfilePage(request):
    if request.method == "GET":
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search)
        return render(request,"Products/allCourse.html",{'courses':course})
    userinfo = get_object_or_404(UserProfile, user=request.user)
    # Get the orders made by the user
    orders = OrdersPayment.objects.filter(user=request.user) 
    # Extract the course IDs from the orders
    course = [order.buycourse for order in orders]
    # Get the courses bought by the user
    courses = Course.objects.filter(courseName__in=course)

    eventRegistration = EventRegistration.objects.filter(user=request.user)
    context = {'userinfo': userinfo, 'courses': courses,'events':eventRegistration}
    return render(request, 'UserProfile/userprofile.html',context)

# Update ProfilePage view**************************************************
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

# Product page view for courses and catagories of courses******************
def Products(request):
    if request.method == "GET":
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search) 
        return render(request,"Products/allCourse.html",{'courses':course})
    courses = Course.objects.order_by('-studentOnCourse')[:6] # Get the top 6 course by user purchased count..
    category_counts = Category.objects.annotate(course_count=Count('course')) # get the catagory courses in the page....
    context = {'courses':courses, 'categories':category_counts}
    return render(request, 'Products/productPage.html',context)

# All Courses page view****************************************************
def AllCourses(request):
    if request.method == "GET":
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search)
        return render(request,"Products/allCourse.html",{'courses':course})
    courses = Course.objects.order_by('-studentOnCourse') # get the all courses bu student count in all course page............. 
    context = {'courses':courses}
    return render(request,"Products/allCourse.html",context)

# View for specefic products About page******************************************
def ProductView(request,id):
    if request.method == "GET":
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search)
        return render(request,"Products/allCourse.html",{'courses':course})
    view =Course.objects.get(id=id) # Get the course about page......
    return render(request,'Products/productview.html',{'view':view})

# view for All products of diffrent categories******************************
def CategoryCourses(request,id):
    try:
        category = Category.objects.get(id=id)
        courses = Course.objects.filter(courseCategory=category) # get all the courses by same categories name............
        context = {'courses': courses, 'category': category}
        return render(request, 'Products/categoryView.html', context)
    except Category.DoesNotExist:
        context = {'error_message': 'Category Courses not found.'}
        return render(request, 'Products/categoryView.html', context)

# Events Page view**********************************************************
def EventPage(request):
    events = Event.objects.all().order_by('-id') #get the events list form database....
    if request.user.is_authenticated:
        registrations = EventRegistration.objects.filter(user=request.user) #check if user authenticated then show the register on event button....
    
    # Create a dictionary to store registered event titles
        registered_events = {}
        for registration in registrations:
            registered_events[registration.event.title] = True  #check if the user participate in the event then dont show apply button again...
        return render(request, 'EventsPage/eventPage.html', {'events': events, 'registered_events': registered_events})
    else:
         return render(request, 'EventsPage/eventPage.html', {'events': events})

# About Info Page view******************************************************
def EventInfo(request, id):
    event = Event.objects.get(id=id)
    if request.user.is_authenticated:
        registrations = EventRegistration.objects.filter(user=request.user) # Same concept as EventPage...........
    
    # Create a dictionary to store registered event titles
        registered_events = {}
        for registration in registrations:
            registered_events[registration.event.title] = True
        return render(request, 'EventsPage/aboutEvent.html', {'event': event, 'registered_events': registered_events})
    else:
        return render(request, 'EventsPage/aboutEvent.html', {'event': event})

# Event registration Form***************************************************
@login_required
def EventRegistrations(request,id):
   events = Event.objects.get(id=id)
   if request.method=="POST":
        registration = EventRegistration(user = request.user,event=events)
        registration.save()
        events.participants += 1
        events.save()  # Save the user info in event Registration when user apply
        messages.success(request,"your application has been submitted!")
   return render(request,'EventsPage/registrationForm.html',{'event':events})

# About Page view***********************************************************
def About(request):
    if request.method == "GET":
      search = request.GET.get('search')
      if search != None:
        course = Course.objects.filter(courseName__icontains=search)
        return render(request,"Products/allCourse.html",{'courses':course})
    return render(request,'About/about.html')

# Payment Intigration payement page*****************************************
@login_required
def PaymentPage(request, id):
    course = Course.objects.get(id = id)
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        courseName = request.POST.get('course')
        referral_code = request.POST.get('referral')
        amount = request.POST.get('amount')
        amount_in_paisa = int(float(amount) * 100)
        discount = 0
        if referral_code!='': # Check if user uses reffral code.....
            try:
                referred_user_profile = UserProfile.objects.get(referral_link=referral_code)   # Check Referral code is matched for any referral code of users...
                discount = 0.2  # 20% discount
                messages.success(request,"Code is applied, You got 20% discount!!!")
                referred_user_profile.referral_code_used += 1  # then add used reffral code field of user by one...........
                referred_user_profile.save()  
            except UserProfile.DoesNotExist:
                messages.error(request,"The code is not applied check the code again...")
        discounted_amount = amount_in_paisa * (1 - discount)
        display_amount = int(discounted_amount/100)
        client = razorpay.Client(auth=('rzp_test_MbEdcN38jYl5CD','LBTeBzDD6GDr3OJujxqHHELX')) #add razor payment gateway.....
        payment = client.order.create({
        'amount': discounted_amount,
        'currency': 'INR',
        'payment_capture': '1'
        })
        Orderspayment = OrdersPayment(user=user,name=name, email=email, buycourse=courseName, amount=amount, payment_id=payment['id'])
        Orderspayment.save()
        course = Course.objects.get(courseName=courseName)  # Save the orders detail and user info in the database.
                
                # Increment the studentOnCourse field by 1
        course.studentOnCourse += 1
        course.save()

        return render(request,'Payment/checkPayment.html',{'payment':payment,'course':course,'discount':display_amount})
    return render(request,'Payment/paymentpage.html',{'course':course})

# Payment Success Page view*************************************************
@csrf_exempt
def PaymentSuccess(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        if order_id:
            order_payment = OrdersPayment.objects.filter(payment_id=order_id).first()
            if order_payment:
                if not order_payment.paid:
                    order_payment.paid = True
                    order_payment.save() #check if the user paid for the course and then save the paid field true.......
                    
                    # Update sales report
                    current_date = datetime.now().date()
                    one_week_ago = current_date - timedelta(days=7)
                    one_month_ago = current_date - timedelta(days=30)
                    one_year_ago = current_date - timedelta(days=365)

                    # Fetch or create Sales object
                    sales_report, created = Sales.objects.get_or_create(pk=1)  

                    # One day sales
                    one_day_sales = OrdersPayment.objects.filter(user=order_payment.user, paid=True, id=order_payment.id).aggregate(total=Sum('amount'))['total'] or 0
                    # One week sales
                    one_week_sales = OrdersPayment.objects.filter(user=order_payment.user, paid=True, id=order_payment.id).aggregate(total=Sum('amount'))['total'] or 0
                    # One month sales
                    one_month_sales = OrdersPayment.objects.filter(user=order_payment.user, paid=True, id=order_payment.id).aggregate(total=Sum('amount'))['total'] or 0
                    # One year sales
                    one_year_sales = OrdersPayment.objects.filter(user=order_payment.user, paid=True, id=order_payment.id).aggregate(total=Sum('amount'))['total'] or 0
                    # Lifetime sales related to the current course purchased by the user
                    lifetime_sales = int(order_payment.amount)  # Assuming amount field stores the payment amount

                    # Update Sales model
                    sales_report.one_day_sale += one_day_sales
                    sales_report.one_week_sale += one_week_sales
                    sales_report.one_month_sale += one_month_sales
                    sales_report.one_year_sale += one_year_sales
                    sales_report.lifetime_sale += lifetime_sales
                    sales_report.save()

                    return render(request, 'Payment/success.html')
                else:
                    return HttpResponseBadRequest("Order already paid")
            else:
                return HttpResponseBadRequest("Invalid order ID")
        else:
            return HttpResponseBadRequest("No razorpay_order_id found in the POST data")

    return HttpResponseNotAllowed(["POST"])

# Send email activation mail for signup varification************************************************
def send_activation_email(user,request):
    current_site = get_current_site(request) 
    email_subject = 'Activate Your Account'
    email_body = render_to_string('login-signup/activate.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject,
                 body=email_body,
                 from_email=settings.EMAIL_FROM_USER,
                 to=[user.email]
                 )
    EmailThread(email).start() #pass the email send mathod to the thread to excution behind the page......

# User Signup view**********************************************************
@csrf_exempt
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
        if (len(password)<6):
            messages.error(request, "Password is too small use min. 6 number of password! ")
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
        send_activation_email(user,request)

        # Generate random referral code for every user
        random_numbers = ''.join(random.choices('0123456789', k=3))
        referral_code = f"{user.first_name}@{user.email[2:10:2]}{random_numbers}"
        
        # Assign random referral code to UserProfile of user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.referral_link = referral_code
        user_profile.save()

        messages.success(request, "We sent you an email verify yor account!")
        return redirect("/login/")

    return render(request, "login-signup/signup.html")

# User Login view***********************************************************
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
        user_profile = UserProfile.objects.get(user=user)
        if not user_profile.is_email_varified:
            messages.error(request,"Your Email not varified, please check the email we sent!")
            return render(request, "login-signup/login.html")
        # Login the user
        if user is None:
            messages.error(request, 'Invalid Password!')
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/")

    return render(request, "login-signup/login.html")

# User Logout View**********************************************************
def UserLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    return HttpResponse('<h1>Error 404 - Page not found!</h1>')

# check if user varify by gmail or not ***************************************************
def activate_user(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    
    if user and generate_token.check_token(user,token):
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_email_varified = True
        user_profile.save()
        messages.success(request,"Your email is varified...")
        return redirect('/login/')
    return render(request,'login-signup/activate_failed.html',{'user':user})