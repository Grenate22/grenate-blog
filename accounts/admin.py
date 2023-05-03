from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Profile
from .forms import CustomUserCreationForm, UpdateUserForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=UpdateUserForm
    model=CustomUser
    list_display= ['email','username','is_staff']
    #fieldsets=UserAdmin.fieldsets + ((None,{'fields':('age',)}),)
    #add_fieldsets=UserAdmin.add_fieldsets + ((None,{'fields':('age',)}),)
# make a class Profileadmin to inherit from class admin and modeladmin which give us control over the look on the admin board
class ProfileAdmin(admin.ModelAdmin):
    #display the field we want to see on the admin profile table
    list_display = ('username','full_name')
#then we register the two 
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Profile,ProfileAdmin)