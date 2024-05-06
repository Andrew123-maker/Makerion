from django.urls import path
from . import views

urlpatterns = [
  path('', views.post_list, name='post_list'),
  path('sports/', views.sports_discussion, name='sport_discussion'),
  path('post/<int:pk>/', views.post_detail, name='post_detail'),
  path('sports/post/<int:pk>/', views.sport_detail, name='post_detail'),
]