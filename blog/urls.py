from django.urls import path
from . import views

urlpatterns = [
  path('', views.post_list, name='post_list'),
  path('post/<int:pk>/', views.post_detail, name='post_detail'),
  path('tag/<slug:tag_slug>/', views.tag, name='tags'),
  path('post/new/', views.post_new, name='post_new'),
]