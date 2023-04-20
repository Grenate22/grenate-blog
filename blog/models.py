from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from datetime import datetime
import uuid
# Create your models here.
class Post(models.Model):
    # i add the id field to give me control over my url to give me a irregular url so hacker cant use that to guess how many number of pages i have
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title= models.CharField(max_length=200)
    author= models.ForeignKey('blog.CustomUser',on_delete=models.CASCADE)
    body= models.TextField()
    date= models.DateTimeField(default=timezone.localtime,blank=True)
    picture = models.ImageField(upload_to='covers/', blank=True)
    #we use this meta to give access to user that can query the database
    class Meta:
        permissions = [
            ('special_status','can read all books')
        ]


    def __str__(self) :
        return self.title
    
    def get_absolute_url(self):
        return reverse ('details',args=[str(self.id)])

#abstractuser allow you to modify the customuser django give us 
class CustomUser(AbstractUser):
    age=models.PositiveIntegerField(null=True,blank=True)
    firstname=models.CharField(max_length=20,null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    comment = models.CharField(max_length=150)
    author = models.ForeignKey('blog.CustomUser',on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('home',args=[str(self.id)])