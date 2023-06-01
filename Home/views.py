from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Post,Tag
from .forms import BlogSearchForm

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
    return render(request, 'Home/home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    latest_posts = Post.objects.order_by('-creation_datetime')[:3]
    tag = Tag.objects.all()
    context = {
        'post': post,
        'latest_posts':latest_posts,
        'tag':tag
    }
    return render(request, 'Home/post_detail.html', context)

def tag_posts(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    tag_posts = Post.objects.filter(tag=tag)
    all_posts = Post.objects.all()
    context = {
        'tag': tag,
        'tag_posts': tag_posts,
        'all_posts': all_posts
    }
    return render(request, 'Home/tag_posts.html', context)


def search(request):
    all_posts = Post.objects.all()
    form = BlogSearchForm()
    results = []
    search_term = None  # 初始化搜索关键字为None
    if request.method == 'POST':
        form = BlogSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            results = list(Post.objects.filter(title__icontains=search_term))
    return render(request, 'Home/search_results.html', {'form': form, 'results': results, 'keyword': search_term})
# class Home(TemplateView):
#     template_name = 'home1.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_blogs'] = Post.objects.all().order_by('-creation_datetime')[:5]
