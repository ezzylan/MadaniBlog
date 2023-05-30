from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from Home.models import Post
from .forms import AddBlogPostForm
from django.contrib.auth import authenticate,login,mixins
from django.contrib.auth.models import User
from django.db.models import Count


# Create your views here.
def blogView(request):
    context = {
        'user': request.user
    }
    return render(request, 'personal/listBlog.html', context)

class BlogPostList(mixins.LoginRequiredMixin,generic.ListView):
    login_url = 'personal/login.html'
    template_name = 'personal/listBlog.html'
    context_object_name = 'personal_post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).annotate(num_fav=Count("blogger")).order_by("-modification_datetime")

class AddPostView(mixins.LoginRequiredMixin,generic.TemplateView):
    login_url = 'personal/login.html'
    template_name = "personal/addBlog.html"

    def get(self, request):
        form = AddBlogPostForm()
        posts = Post.objects.filter(author=request.user)
        args={
            'form':form,
            'posts':posts
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = AddBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            video = form.cleaned_data['video']
            args={
                'form': form,
                'title': title,
                'content': content,
                'image': image,
                'video': video
            }
        return HttpResponseRedirect(reverse('personal:add'))


