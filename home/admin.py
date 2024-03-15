from django.contrib import admin                      

# Register your models here.
from .models import UserProfile,Course,Category

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','referral_link']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseName','coursePrice','madeBy','courseDuration','studentOnCourse']

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('categoryName',)  # Tuple with the field name

admin.site.register(Category, CategoryAdmin)