from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import User
from datetime import datetime


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=None, null=True, default='null')
    video = models.FileField(upload_to=None, null=True, default='null')
    creation_datetime = models.DateTimeField(auto_now=True)
    modification_datetime = models.DateTimeField(
        default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if datetime.now().astimezone() > self.modification_datetime:
            self.modification_datetime = datetime.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    published_date = models.DateTimeField(auto_now=True)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    profile_image = models.ImageField(upload_to=None)
    following_users = models.ManyToManyField(
        User, related_name="following_user", default='null')
    follower = models.ManyToManyField(
        User, related_name='follower', default='null')
    fav_post = models.ManyToManyField(Post, default='null')
