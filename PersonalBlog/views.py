from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from Home.models import Post
from .forms import AddBlogPostForm
from .forms import AddCommentsForm
from .forms import CreateBlog
from django.contrib.auth import authenticate,login,mixins
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages

# Create your views here.
def blogView(request):
    context = {
        'user': request.user
    }
    return render(request, 'personal/listBlog.html', context)

class BlogPostList(mixins.LoginRequiredMixin,generic.ListView):
    login_url = '/personal/login/'
    template_name = 'personal/listBlog.html'
    context_object_name = 'personal_post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).annotate(num_fav=Count("blogger")).order_by("-modification_datetime")

class ManagePostList(mixins.LoginRequiredMixin,generic.ListView):
    login_url = '/personal/login/'
    template_name = 'personal/manageBlogList.html'
    context_object_name = 'personal_post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-modification_datetime")

class AddPostView(mixins.LoginRequiredMixin,generic.TemplateView):
    login_url = '/personal/login/'
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
        return HttpResponseRedirect(reverse('Personal:view'))

class PostCommentDetailView(mixins.LoginRequiredMixin,generic.TemplateView):
    login_url = '/personal/login/'
    template_name = "personal/postDetail.html"

    def get(self,request,slug):
        form = AddCommentsForm()
        posts = Post.objects.filter(author=request.user).annotate(num_fav=Count("blogger"))
        postBySlug = Post.objects.filter(slug=slug)
        args = {
            'form': form,
            'posts': posts,
            'postBySlug':postBySlug
        }
        return render(request, self.template_name, args)

    def post(self, request, slug):
        form = AddCommentsForm(request.POST)
        if form.is_valid():
            commentForm = form.save(commit=False)
            commentForm.blogger = request.user
            commentForm.post = Post.objects.filter(slug=slug).first()
            commentForm.save()
            comment = form.cleaned_data['comment']
            args={
                'form': form,
                'comment':comment
            }
        return HttpResponseRedirect(reverse('Personal:postDetail', kwargs={'slug':slug}))

class editPostView(mixins.LoginRequiredMixin,generic.TemplateView):
    login_url = '/personal/login/'
    template_name = "personal/editPost.html"

    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        posts = Post.objects.filter(author=request.user).annotate(num_fav=Count("blogger"))
        form = AddBlogPostForm(instance=post)
        args = {
            'form': form,
            'posts': posts,
            'post':post
        }

        return render(request, self.template_name, args)

    def post(self, request, slug):
        post = Post.objects.filter(slug=slug).first()
        form = AddBlogPostForm(request.POST,instance=post)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return HttpResponseRedirect(reverse('Personal:manage'))
        else:
            messages.error(request, 'Please correct the following errors:')
            return HttpResponseRedirect(reverse('Personal:postDetail', kwargs={'slug':slug}))

def deletePostView(request,slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return HttpResponseRedirect(reverse('Personal:manage'))

class AddBlogView(mixins.LoginRequiredMixin,generic.TemplateView):
    login_url = '/personal/login/'
    template_name = "personal/createBlog.html"

    def get(self, request):
        form = CreateBlog()
        args={
            'form':form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = AddBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = request.user.profile
            blogform = form.save(request.POST,instance=blog)
            blogform.save()
            blog_title = blogform.cleaned_data['blog_title']
            blog_description = blogform.cleaned_data['blog_description']
            blog_image = blogform.cleaned_data['blog_image']
            args={
                'form': blogform,
                'blog_title': blog_title,
                'blog_description': blog_description,
                'blog_image': blog_image
            }
        return HttpResponseRedirect(reverse('Personal:view'))