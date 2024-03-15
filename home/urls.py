
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home, name='home'),
    path('login/',views.UserLogin, name='login'),
    path('signup/',views.UserSignup, name='signup'),
    path('logout/',views.UserLogout, name='logout'),
    path('profilePage/',views.ProfilePage, name='profilePage'),
    path('updateProfile/',views.updateProfile, name='updateProfile'),
    path('product/',views.Products, name='Products'),
    path('allCourses/',views.AllCourses, name='allCourses'),
    path('productView/<slug:id>',views.ProductView, name='productView'),
    path('courses/<slug:id>',views.CategoryCourses, name='courses'),
    path('about/',views.About, name='about'),
]
