from django.contrib import admin
from django.contrib.auth.models import User
from .models import Tag,Post,Follow,Comment, Profile


#mix profile info into user info
class ProfileInline(admin.StackedInline):
  model = Profile

class UserAdmin(admin.ModelAdmin):
  model = User
  fields = ['username', 'password']
  inlines =[ProfileInline]
  
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Profile)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)