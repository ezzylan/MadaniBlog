from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="home"),
    path('tag/<int:tag_id>/', views.tag_posts, name='tag_posts'),
]