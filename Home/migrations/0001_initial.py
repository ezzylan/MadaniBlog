# Generated by Django 4.2.1 on 2023-05-29 16:15

import Home.models
import autoslug.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.post')),
            ],
        ),
        migrations.CreateModel(
            name='Blogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='/static/images/placeholder-profile-icon.jpg', upload_to=Home.models.user_directory_path)),
                ('tagline', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('twitter_link', models.URLField(blank=True)),
                ('instagram_link', models.URLField(blank=True)),
                ('facebook_link', models.URLField(blank=True)),
                ('website_link', models.URLField(blank=True)),
                ('blog_title', models.CharField(max_length=500)),
                ('blog_description', models.TextField(blank=True)),
                ('blog_image', models.ImageField(blank=True, upload_to=Home.models.user_directory_path)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user')),
                ('fav_post', models.ManyToManyField(default='null', to='Home.post')),
                ('follower', models.ManyToManyField(default='null', related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following_users', models.ManyToManyField(default='null', related_name='following_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
