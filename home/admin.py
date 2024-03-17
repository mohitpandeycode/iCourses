from django.contrib import admin                      

# Register your models here.
from .models import UserProfile,Course,Category,OrdersPayment,Event,EventRegistration,Sales

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','referral_link']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseName','coursePrice','madeBy','courseDuration','studentOnCourse']

@admin.register(OrdersPayment)
class OrdersPaymentAdmin(admin.ModelAdmin):
    list_display = ['name','email','buycourse','amount']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title','date','time','participants','organizer']

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['one_day_sale','one_week_sale','one_month_sale','one_year_sale','lifetime_sale']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user','event']

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('categoryName',)  # Tuple with the field name
admin.site.register(Category, CategoryAdmin)