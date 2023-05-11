from django import forms
from .models import Post,Category,Comment

choices = Category.objects.all().values_list('name','name')
choice_list = []
for item in choices:
     choice_list.append(item)
class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title','body','picture','status','tags']

            widgets = {
                  'title' : forms.TextInput(attrs={'class': 'form-control'}),
                  'category' : forms.Select (choices=choice_list, attrs={'class': 'form-control'}),
                  'body' : forms.Textarea(attrs={'class': 'form-control','rows':3}),
                  'picture' : forms.FileInput(attrs={'class': 'form-control'}),
                  'status' : forms.CheckboxInput(attrs={'class': 'form-control'}),
                  'tags' : forms.TextInput(attrs={'class': 'form-control'}),
                  
            }

class CommentForm(forms.ModelForm):
      class Meta:
            model = Comment
            fields = ['comment']

            widgets = {
                  'comment' : forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            }
      