from django.forms import ModelForm
from Home.models import Post
from django import forms

class AddBlogPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'creation_datetime', 'modification_datetime']
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'image': 'Post Image',
            'video': 'Post Video'
        }
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control '}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control w-50'}),
            'video':forms.FileInput(attrs={'class':'form-control w-50'})
        }