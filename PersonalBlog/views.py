from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from Home.models import Post
from Home.models import Blogger
from .forms import AddBlogPostForm
from .forms import AddCommentsForm
from .forms import CreateBlog
from django.contrib.auth import authenticate, login, mixins
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Count
from django.contrib import messages


# Create your views here.
def blogView(request):
    context = {
        'user': request.user
    }
    return render(request, 'personal/listBlog.html', context)


def register_login(request):
    if request.POST.get('submit') == 'sign_up':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            form = UserCreationForm()
            messages.success(request, "Account was created for " + user + ". Please login again")
            return HttpResponseRedirect(reverse('Home:home'))
        else:
            messages.error(request, 'Please correct the following errors')
            return HttpResponseRedirect(reverse('Personal:loginregister'))

    elif request.POST.get('submit') == 'sign_in':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'home/home.html')
        else:
            messages.info(request, 'Wrong username or password')
            return HttpResponseRedirect(reverse('Personal:loginregister'))
    return HttpResponseRedirect(reverse('Personal:loginregister'))


class BlogPostList(mixins.LoginRequiredMixin, generic.ListView):
    login_url = '/personal/login/'
    template_name = 'personal/listBlog.html'
    context_object_name = 'personal_post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).annotate(num_fav=Count("blogger")).order_by(
            "-modification_datetime")


def BlogPostOther(request, pk):
    post_list = Post.objects.filter(author__pk=pk).annotate(num_fav=Count("blogger")).order_by("-modification_datetime")
    blogger = Blogger.objects.filter(user_id=pk)
    context = {
        'post_list': post_list,
        'profile': blogger
    }
    return render(request, 'personal/otherPersonalBlog.html', context)


class ManagePostList(mixins.LoginRequiredMixin, generic.ListView):
    login_url = '/personal/login/'
    template_name = 'personal/manageBlogList.html'
    context_object_name = 'personal_post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-modification_datetime")


class AddPostView(mixins.LoginRequiredMixin, generic.TemplateView):
    login_url = '/personal/loginregister/'
    template_name = "personal/addBlog.html"

    def get(self, request):
        form = AddBlogPostForm()
        posts = Post.objects.filter(author=request.user)
        args = {
            'form': form,
            'posts': posts
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = AddBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            print(form)
            post.author = request.user
            post.save()
            form.save_m2m()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            args = {
                'form': form,
                'title': title,
                'content': content,
                'image': image
            }
            return HttpResponseRedirect(reverse('Personal:view'))
        else:
            messages.error(request, 'Unable to add new post, please find error shown')
            return render(request, 'personal/addBlog.html', {'form': form})


class PostCommentDetailView(mixins.LoginRequiredMixin, generic.TemplateView):
    login_url = '/personal/loginregister/'
    template_name = "personal/postDetail.html"

    def get(self, request, slug):
        form = AddCommentsForm()
        posts = Post.objects.filter(author=request.user).annotate(num_fav=Count("blogger"))
        postBySlug = Post.objects.get(slug=slug)
        fav = postBySlug.blogger_set.filter(user=request.user)
        args = {
            'form': form,
            'posts': posts,
            'singlePost': postBySlug,
            'fav': fav
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
            args = {
                'form': form,
                'comment': comment
            }
        return HttpResponseRedirect(reverse('Personal:postDetail', kwargs={'slug': slug}))


class editPostView(mixins.LoginRequiredMixin, generic.TemplateView):
    login_url = '/personal/login/'
    template_name = "personal/editPost.html"

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        posts = Post.objects.filter(author=request.user).annotate(num_fav=Count("blogger"))
        form = AddBlogPostForm(instance=post)
        args = {
            'form': form,
            'posts': posts,
            'post': post
        }

        return render(request, self.template_name, args)

    def post(self, request, slug):
        post = Post.objects.filter(slug=slug).first()
        form = AddBlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return HttpResponseRedirect(reverse('Personal:manage'))
        else:
            messages.error(request, 'Please correct the following errors')
            return HttpResponseRedirect(reverse('Personal:postDetail', kwargs={'slug': slug}))


def deletePostView(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return HttpResponseRedirect(reverse('Personal:manage'))


class AddBlogView(mixins.LoginRequiredMixin, generic.TemplateView):
    login_url = '/personal/login/'
    template_name = "personal/createEditBlog.html"

    def get(self, request):
        blog = Blogger.objects.filter(user=request.user).first()
        form = CreateBlog(instance=blog)
        args = {
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        blog = Blogger.objects.filter(user=request.user).first()
        form = CreateBlog(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            blog_title = form.cleaned_data['blog_title']
            blog_description = form.cleaned_data['blog_description']
            blog_image = form.cleaned_data['blog_image']
            args = {
                'form': form,
                'blog_title': blog_title,
                'blog_description': blog_description,
                'blog_image': blog_image
            }
            return HttpResponseRedirect(reverse('Profile:profile', kwargs={'slug': blog.slug}))
        else:
            messages.error(request, 'Unable to create blog, please find error shown')
            return render(request, 'personal/createEditBlog.html', {'form': form})


def favView(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if (request.POST.get('fav') == 'yes'):
        request.user.blogger.fav_post.add(post)
    else:
        request.user.blogger.fav_post.remove(post)
    return HttpResponseRedirect(reverse('Personal:postDetail', kwargs={'slug': post.slug}))
