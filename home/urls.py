
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.Home, name='home'),
    path('login/',views.UserLogin, name='login'),
    path('activate_user/<uidb64>/<token>',views.activate_user, name='activate'),
    path('signup/',views.UserSignup, name='signup'),
    path('logout/',views.UserLogout, name='logout'),
    path('profilePage/',views.ProfilePage, name='profilePage'),
    path('updateProfile/',views.updateProfile, name='updateProfile'),
    path('product/',views.Products, name='Products'),
    path('allCourses/',views.AllCourses, name='allCourses'),
    path('productView/<slug:id>',views.ProductView, name='productView'),
    path('courses/<slug:id>',views.CategoryCourses, name='courses'),
    path('events/',views.EventPage, name='events'),
    path('eventInfo/<slug:id>',views.EventInfo, name='eventInfo'),
    path('eventRegistration/<slug:id>',views.EventRegistrations, name='eventRegistration'),
    path('paymentPage/<slug:id>',views.PaymentPage, name='paymentPage'),
    path('paymentSuccess/',views.PaymentSuccess, name='paymentSuccess'),
    path('about/',views.About, name='about'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)