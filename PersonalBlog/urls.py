from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('list/',views.blogView,name='view'),
    path('list/',views.BlogPostList.as_view(),name='view'),
    path('manage/',views.ManagePostList.as_view(),name='manage'),
    path('add/',views.AddPostView.as_view(),name='add'),
    path('post/<slug:slug>/',views.PostCommentDetailView.as_view(),name='postDetail'),
    path('post/edit/<slug:slug>/', views.editPostView.as_view(), name='postEdit'),
    path('post/delete/<slug:slug>/', views.deletePostView, name='postDelete'),
    path('login/',auth_views.LoginView.as_view(template_name = 'personal/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]