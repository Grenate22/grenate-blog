from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from accounts.models import Profile
import uuid
from PIL import Image
# Create your models here.
class Post(models.Model):
    # i add the id field to give me control over my url to give me a irregular url so hacker cant use that to guess how many number of pages i have
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title= models.CharField(max_length=200)
    author= models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    body= models.TextField()
    category = models.CharField(max_length=200, default='coding')
    date= models.DateTimeField(default=timezone.localtime,blank=True)
    picture = models.ImageField(upload_to='covers/', blank=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE , null=True ,blank=True)
    likes = models.ManyToManyField('accounts.CustomUser', related_name='blog_posts')
   
    #we use this meta to give access to user that can query the database
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

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('details',kwargs={'pk': str(self.pk)})
    
    