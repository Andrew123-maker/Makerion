from django.shortcuts import render, get_object_or_404
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.utils import timezone
from .models import Post, Tag, Profile
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def post_list(request):
  if 'q' in request.GET:
    q = request.GET['q']
    multiple_q = Q(tag__title__icontains=q) | Q(title__icontains=q)
    posts = Post.objects.filter(multiple_q).order_by('published_date').distinct()
  else:
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').distinct()
  context = {'posts':posts}
  return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
  if request.method == "POST":
      form = PostForm(request.POST, request.FILES)
      if form.is_valid():
          image = form.cleaned_data['image']
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
          tag = form.cleaned_data['tag']
          likes = form.cleaned_data['likes']
          post = Post.objects.create(
            user=request.user,
            title=title,
            text=text,
            likes=likes,
            image=image,
            published_date=timezone.now()
          )
          post.tag.set(tag)
          post.save()
          return redirect('post_detail', pk=post.pk)
  else:
      form = PostForm()
  return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.published_date = timezone.now()
        post.save()
        return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm(instance=post)
  return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_delete(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.delete()
  return redirect('post_list')

def add_comment_to_post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post= post
      comment.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = CommentForm()
  return render(request, 'blog/add_comment_to_post.html', {'form':form})

def user_profile(request):
  profile = get_object_or_404(Profile, user=request.user)
  return render(request, 'blog/user_profile.html', {'profile':profile})