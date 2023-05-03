from django import forms
from .models import Post,Category

choices = Category.objects.all().values_list('name','name')
choice_list = []
for item in choices:
     choice_list.append(item)
class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title','category','body','picture']

            widgets = {
                  'title' : forms.TextInput(attrs={'class': 'form-control'}),
                  'category' : forms.Select (choices=choice_list, attrs={'class': 'form-control'}),
                  'body' : forms.Textarea(attrs={'class': 'form-control'}),
                  'picture' : forms.FileInput(attrs={'class': 'form-control'}),
                  
            }

        
