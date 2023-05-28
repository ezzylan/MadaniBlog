from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=None, null=True, default="null")
    video = models.FileField(upload_to=None, null=True, default="null")
    creation_datetime = models.DateTimeField(auto_now=True)
    modification_datetime = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        self.modification_datetime = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title;

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    published_date = models.DateTimeField(auto_now=True)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images/")

    # social links
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    # blog info
    blog_title = models.CharField(max_length=500)
    blog_description = models.TextField(max_length=500, blank=True)
    blog_image = models.ImageField(upload_to="blog_images/")

    following_users = models.ManyToManyField(
        User, related_name="following_user", default="null"
    )
    follower = models.ManyToManyField(User, related_name="follower", default="null")
    fav_post = models.ManyToManyField(Post, default="null")
    slug = models.SlugField(max_length=150, default='null')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)
