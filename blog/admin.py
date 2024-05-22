from django.contrib import admin
from PIL import Image
from .models import Tag,Post,Follow,Comment

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)