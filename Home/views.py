from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Post,Tag


def post_list(request):
    latest_posts = Post.objects.order_by('-creation_datetime')[:5]
    popular_posts = Post.objects.order_by('-modification_datetime')[:5]
    all_posts = Post.objects.all()
    tag = Tag.objects.all()
    context = {
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,
        'all_posts': all_posts,
        'tag':tag
    }
    return render(request, 'home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    latest_posts = Post.objects.order_by('-creation_datetime')[:3]
    tag = Tag.objects.all()
    context = {
        'post': post,
        'latest_posts':latest_posts,
        'tag':tag
    }
    return render(request, 'post_detail.html', context)

def tag_posts(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    tag_posts = Post.objects.filter(tag=tag)
    all_posts = Post.objects.all()
    context = {
        'tag': tag,
        'tag_posts': tag_posts,
        'all_posts': all_posts
    }
    return render(request, 'tag_posts.html', context)

# class Home(TemplateView):
#     template_name = 'home1.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_blogs'] = Post.objects.all().order_by('-creation_datetime')[:5]
