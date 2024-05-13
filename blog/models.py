from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.utils import timezone
from django.utils.text import slugify 
from django.urls import reverse
import uuid
from django.db.models.signals import post_save, post_delete

# uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


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
  image = ImageField(default="default.jpg", blank=True)
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

class Follow(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Stream(models.Model):
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post', null=True)
  published_date = models.DateTimeField(blank=True, null=True)
  
  def add_post(sender, instance, *args, **kwargs):
    post = instance
    user = post.user
    followers = Follow.objects.all().filter(following=user)
    for follower in followers:
      stream = Stream(post=post,user=follower.follower, published_date=post.published_date, following=user)
      stream.save()


#
post_save.connect(Stream.add_post, sender=Post)