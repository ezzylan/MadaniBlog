from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('list/',views.blogView,name='view'),
    path('list/',views.BlogPostList.as_view(),name='view'),
    path('add/',views.AddPostView.as_view(),name='add'),
    path('login/',auth_views.LoginView.as_view(template_name = 'personal/login.html'),name='login')
]