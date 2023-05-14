from django import forms
from .models import Post,Comment


class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title','body','picture','tags']

            widgets = {
                  'title' : forms.TextInput(attrs={'class': 'form-control'}),
                  'body' : forms.Textarea(attrs={'class': 'form-control','rows':3}),
                  'picture' : forms.FileInput(attrs={'class': 'form-control'}),
                  'tags' : forms.TextInput(attrs={'class': 'form-control'}),
                  
            }

class CommentForm(forms.ModelForm):
      class Meta:
            model = Comment
            fields = ['comment']

            widgets = {
                  'comment' : forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            }
      