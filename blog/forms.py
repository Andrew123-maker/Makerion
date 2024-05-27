from django import forms
from PIL import Image
from django.forms.widgets import ClearableFileInput
from .models import Post, Tag, Comment

choices = Tag.objects.all().values_list('title', 'title')
class PostForm(forms.ModelForm):
  
  class Meta:
    model = Post
    fields=('image','title', 'text', 'tag', 'likes')
    
    widgets = {
      'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
      'title': forms.TextInput(attrs={'class':'form-control'}),
      'tag': forms.SelectMultiple(choices=choices, attrs={'class':'form-control'}),
      'text': forms.Textarea(attrs={'class':'form-control'}),
    }

class CommentForm(forms.ModelForm):
  
  class Meta:
    model = Comment
    fields=('user','text')
    widgets = {
      'user': forms.TextInput(attrs={'class':'form-control'}),
      'text': forms.Textarea(attrs={'class':'form-control'}),
    }
    
