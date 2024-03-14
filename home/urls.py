
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home, name='home'),
    path('login/',views.UserLogin, name='login'),
    path('signup/',views.UserSignup, name='signup'),
    path('logout/',views.UserLogout, name='logout'),
    path('profilePage/',views.ProfilePage, name='profilePage'),
]
