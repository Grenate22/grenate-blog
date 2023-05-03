from django.contrib import admin
from .models import Post,Comment,Category
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

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category)
