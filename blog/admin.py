from django.contrib import admin
from .models import Post,Comment
# Register your models here.
class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]
    list_display = ('title','author','date')
    list_filter = ('status','date','author')
    search_fields = ('title','body')
    raw_id_fields = ('author',)
    date_hierarchy = 'date'
    ordering = ('status','date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','comment','author')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
