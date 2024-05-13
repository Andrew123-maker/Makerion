from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Tag
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/post_detail.html', {'post':post})

def tag(request, tag_slug):
  tag = get_object_or_404(Tag, slug=tag_slug)
  posts = Post.objects.filter(tag=tag).order_by('-published_date')
  context={
    'tag': tag
  }
  return render(request, tag.html, context)

def post_new(request):
  if request.method == "POST":
      form = PostForm(request.POST)
      if form.is_valid():
          post = form.save(commit=False)
          post.author = request.user
          post.published_date = timezone.now()
          post.save()
          return redirect('post_detail', pk=post.pk)
  else:
      form = PostForm()
  return render(request, 'blog/post_edit.html', {'form': form})

