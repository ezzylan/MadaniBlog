from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from autoslug import AutoSlugField


def user_directory_path(instance, filename):
    if isinstance(instance, Post):
        return "user_{0}/posts/{1}".format(instance.user.id, filename)
    elif isinstance(instance, Blogger):
        return "user_{0}/bloggers/{1}".format(instance.user.id, filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, null=True, default="null")
    video = models.FileField(upload_to=user_directory_path, null=True, default="null")
    creation_datetime = models.DateTimeField(auto_now=True)
    modification_datetime = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        self.modification_datetime = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    published_date = models.DateTimeField(auto_now=True)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to=user_directory_path,
        default=static("images/placeholder-profile-icon.jpg"),
    )
    tagline = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    # social links
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    # blog info
    blog_title = models.CharField(max_length=500)
    blog_description = models.TextField(blank=True)
    blog_image = models.ImageField(upload_to=user_directory_path, blank=True)

    following_users = models.ManyToManyField(
        User, related_name="following_user", default="null"
    )
    follower = models.ManyToManyField(User, related_name="follower", default="null")
    fav_post = models.ManyToManyField(Post, default="null")
    slug = AutoSlugField(populate_from="user")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
