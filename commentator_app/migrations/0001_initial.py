# Generated by Django 4.1.4 on 2022-12-17 04:11

import commentator_app.validators.files
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Username')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('home_page', models.URLField(blank=True, verbose_name='Home page')),
                ('text', models.TextField(max_length=2048, verbose_name='Comment text')),
                ('file', models.FileField(blank=True, upload_to='uploads/commentator/%Y/%m/%d', validators=[commentator_app.validators.files.FileValidator(content_types=('image/jpeg', 'image/gif', 'image/png', 'text/plain'), max_size=102400)], verbose_name='File')),
                ('is_published', models.BooleanField(default=True, verbose_name='Is published')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reply_to', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='commentator_app.comment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]