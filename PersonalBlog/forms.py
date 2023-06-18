from django.forms import ModelForm
from Home.models import Post
from Home.models import Comment
from Home.models import Blogger
from django.contrib.auth.models import User
from django import forms

class AddBlogPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'creation_datetime', 'modification_datetime','slug']
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'image': 'Post Image',
            'tag':'Hash Tag'
        }
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control '}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.CheckboxSelectMultiple()
        }

class AddCommentsForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'published_datetime', 'blogger','post']
        widgets ={
            'comment':forms.Textarea(attrs={'class':'form-control'})
        }

class CreateBlog(ModelForm):
    class Meta:
        model = Blogger
        exclude = ['user', 'profile_image', 'tagline','bio','twitter_link','instagram_link','facebook_link','website_link',
                                                            'following_users','follower','fav_post','slug']
        widgets ={
             'blog_title': forms.TextInput(attrs={'class': 'form-control '}),
            'blog_description':forms.Textarea(attrs={'class':'form-control'}),
            'blog_image':forms.FileInput(attrs={'class':'form-control w-50'})
        }

class RegisterUser(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})

        }
