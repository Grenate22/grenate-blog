from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
#we import image from PIL i already install a package name pillow
from PIL import Image
# Create your models here.
#abstractuser allow you to modify the built-in User model django give us
#we specify accounts.CustomUser in our settings 
class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    username= models.OneToOneField('accounts.CustomUser',on_delete=models.CASCADE ,related_name="profile")
    full_name = models.CharField(max_length=100)
    website_url = models.URLField(max_length=200,null=True,blank=True)
    facebook_url = models.URLField(max_length=200,null=True,blank=True)
    twitter_url = models.URLField(max_length=200,null=True,blank=True)
    instagram_url = models.URLField(max_length=200,null=True,blank=True)
    linkedln_url = models.URLField(max_length=200,null=True,blank=True)
    
    #we make a default image for our user that they can update later and we specify the path our model will get it we also specify the path we upload to cuz django handle pictures and file seperately 
    avatar = models.ImageField(default='profile_pic/avatar.png/', upload_to='profile_pic/')
    bio = models.TextField()

    def __str__(self) :
        return str(self.username)
    
    def get_absolute_url(self):
        return reverse('profile',kwargs={'pk': str(self.pk)})

    

     #we format the image the user post 
    def save(self,*args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)