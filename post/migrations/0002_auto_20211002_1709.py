# Generated by Django 3.2.7 on 2021-10-02 11:09

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='default/category/default-category.png', null=True, upload_to=post.models.category_directory_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='default/default-post-thumbnail.jpg', upload_to=post.models.post_directory_path),
        ),
    ]