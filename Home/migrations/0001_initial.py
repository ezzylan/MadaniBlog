# Generated by Django 4.2.1 on 2023-06-11 15:27

import Home.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image', models.ImageField(default='null', null=True, upload_to=Home.models.user_directory_path)),
                ('video', models.FileField(default='null', null=True, upload_to=Home.models.user_directory_path)),
                ('creation_datetime', models.DateTimeField(auto_now=True)),
                ('modification_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('slug', models.SlugField(blank=True, default='null', null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tag', models.ManyToManyField(default='null', to='Home.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('blogger', models.ForeignKey(blank=True, default='null', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.post')),
            ],
        ),
        migrations.CreateModel(
            name='Blogger',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_image', models.ImageField(blank=True, upload_to=Home.models.user_directory_path)),
                ('tagline', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('twitter_link', models.URLField(blank=True)),
                ('instagram_link', models.URLField(blank=True)),
                ('facebook_link', models.URLField(blank=True)),
                ('website_link', models.URLField(blank=True)),
                ('blog_title', models.CharField(blank=True, max_length=500, null=True)),
                ('blog_description', models.TextField(blank=True)),
                ('blog_image', models.ImageField(blank=True, upload_to=Home.models.user_directory_path)),
                ('slug', models.SlugField(default='null', unique=True)),
                ('fav_post', models.ManyToManyField(blank=True, default='null', null=True, to='Home.post')),
                ('follower', models.ManyToManyField(blank=True, default='null', null=True, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following_users', models.ManyToManyField(blank=True, default='null', null=True, related_name='following_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
