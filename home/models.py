from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    referral_link = models.CharField(max_length=100,default='', blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    age = models.CharField(max_length=14,null=True,blank=True)