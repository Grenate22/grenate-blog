from django.contrib import admin
from .models import Post,Comment
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    list_display= ['email','username','age','is_staff','password','firstname']
    fieldsets=UserAdmin.fieldsets + ((None,{'fields':('age','firstname')}),)
    add_fieldsets=UserAdmin.add_fieldsets + ((None,{'fields':('age','firstname')}),)
# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]

    list_display = ('title','author','date')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)