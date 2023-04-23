from django.contrib import admin
from .models import Post,Comment,Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, UpdateUserForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=UpdateUserForm
    model=CustomUser
    list_display= ['email','username','is_staff']
    #fieldsets=UserAdmin.fieldsets + ((None,{'fields':('age',)}),)
    #add_fieldsets=UserAdmin.add_fieldsets + ((None,{'fields':('age',)}),)
# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]

    list_display = ('title','author','date')

class CommentAdmin(admin.ModelAdmin):

    list_display = ('post','comment','author')

class ProfileAdmin(admin.ModelAdmin):

    list_display = ('username','full_name')


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Profile,ProfileAdmin)