from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    referral_link = models.CharField(max_length=100,default='', blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    phone = models.CharField(max_length=14, default='', blank=True, null=True)
    address = models.TextField(default='', blank=True, null=True)
    birthdate = models.CharField(max_length =20,null=True, blank=True)
    referral_code_used = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username


class Category(models.Model):
    categoryName = models.CharField(max_length=200)

    def __str__(self):
        return self.categoryName

class Course(models.Model):
    coursePicture = models.ImageField(upload_to='coursePicture',null=True,blank = True)
    courseFile = models.FileField(upload_to='coursePdf',null=True,blank=True)
    courseCategory = models.ForeignKey(Category, on_delete=models.CASCADE ,null=True,blank=True)
    courseName = models.CharField(max_length = 150,null=True,blank=True)
    coursePrice = models.IntegerField(null=True,blank=True)
    madeBy = models.CharField(max_length = 150,null=True,blank=True)
    courseDuration = models.CharField(max_length = 50)
    studentOnCourse = models.IntegerField(default = 0)
    AboutCourse = HTMLField(blank=True)

    def __str__(self) -> str:
        return self.courseName



class OrdersPayment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 200)
    buycourse = models.CharField(max_length=500)
    amount = models.CharField(max_length = 100)
    payment_id = models.CharField(max_length = 150)
    paid = models.BooleanField(default = False)

