from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from accounts.models import Profile
import uuid
from PIL import Image
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
# Create your models here.
class UUIDTaggedItem(GenericUUIDTaggedItemBase,TaggedItemBase):
    class Meta:
        verbose_name = ("Tag")
        verbose_name_plural = ("Tags")

class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    # i add the id field to give me control over my url to give me a irregular url so hacker cant use that to guess how many number of pages i have
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title= models.CharField(max_length=200)
    author= models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    body= RichTextField(blank=True, null=True)
    #body= models.TextField()
    category = models.CharField(max_length=200, default='coding')
    date= models.DateTimeField(default=timezone.localtime,blank=True)
    picture = models.ImageField(upload_to='covers/', blank=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE , null=True ,blank=True)
    status = models.CharField(max_length=2, choices=Status.choices,default=Status.DRAFT)
    likes = models.ManyToManyField('accounts.CustomUser', related_name='blog_posts')
    tags = TaggableManager(through=UUIDTaggedItem)
   
    #we use this meta to give access to user that can query the database
    class Meta:
        indexes = [
            models.Index(fields=['-date']),
        ]
#this return as a string instead of an object on our admin page i also add the str(self.author) cuz just self.author is an object we need to render it as string
    
    def __str__(self):
        return self.title + ' |' + str(self.author)
    
    def total_likes(self):
        return self.likes.count()
    
    
    def get_absolute_url(self):
        return reverse('details',kwargs={'pk': str(self.pk)})
    
    #def get_absolute_url(self):
        #return reverse ('details', kwargs={'slug' : self.slug})
    #def save(self,*args,**kwargs):
        #if not self.slug:
            #self.slug = slugify(self.title)
        #return super(Post,self).save(*args,**kwargs)
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField()
    author = models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('details',kwargs={'pk': str(self.pk)})
    
class PopularPost(models.Model)  :
    title = models.CharField(max_length=200)
    author = models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='covers/', blank=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PopularPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-views')
