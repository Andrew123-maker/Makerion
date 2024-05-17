from django import forms
from PIL import Image
from .models import Post, Tag

class PostForm(forms.ModelForm):
  
  class Meta:
    model = Post
    fields=['image', 'title', 'text', 'tag', 'likes']