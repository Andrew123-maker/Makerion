from re import U
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.utils import timezone
from django.utils.text import slugify 
from django.urls import reverse
import uuid
from PIL import Image
from django.db.models.signals import post_save, post_delete

# uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user, filename)


class Tag(models.Model):
  title = models.CharField(max_length=100,verbose_name="tag")
  slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)
  class Meta:
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'

  def get_absolute_url(self):
    return reverse('tags', args=[self.slug])

  def __str__(self):
    return self.title

  def save(self, *arg, **kwargs):
    if not self.slug:
      self.slug - slugify(self.slug)
    return super().save(*arg, **kwargs)


class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  image = ImageField(blank=True, null=True, upload_to=user_directory_path)
  title = models.CharField(max_length=200)
  text = models.TextField()
  tag = models.ManyToManyField(Tag, related_name='tags')
  likes = models.IntegerField(default = 0)
  created_date = models.DateTimeField(default=timezone.now)
  published_date = models.DateTimeField(blank=True, null=True)

  def publish(self):
    self.published_date = timezone.now()
    self.save()

  def __str__(self):
    return self.title

class Comment(models.Model):
  post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
  user = models.CharField(max_length=200)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  likes = models.IntegerField(default=0)

  def __str__(self):
    return self.text

class Follow(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100, default='name')
  bio = models.TextField(blank=True, null=True)
  image = models.ImageField(default='default.jpg',upload_to=user_directory_path)
  last_update = models.DateTimeField(User, auto_now=True)
  
  def __str__(self):
    return self.user.username

#create profile when new user sign up
def created_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = Profile(user=instance)
    user_profile.save()

post_save.connect(created_profile, sender=User)
