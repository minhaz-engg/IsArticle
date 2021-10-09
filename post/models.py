import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
import os
from django.conf import settings
# Create your models here.
User = get_user_model()

def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    thumbnail_name = f'post/{instance.user}/{instance.post_title}/thumbnail.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return thumbnail_name

def category_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    thumbnail_name = f'category/{instance.name}/thumbnail.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return thumbnail_name

class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("max length 50"),
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_(
        "Category safe URL"), max_length=255, unique=True)
    image = models.ImageField(upload_to=category_directory_path,blank=True, null=True, default="default/category/default-category.png")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CategorySubscribe(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="categora")
    subscribed_category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.subscriber}===>{self.subscribed_category}"


class CustomizedTag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    post_title = models.CharField(max_length=264, verbose_name="Put a Title")
    slug = models.SlugField(max_length=264, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT)
    tags = TaggableManager()
    post_content = RichTextField(null=False)
    thumbnail = models.ImageField(upload_to=post_directory_path,default="default/default-post-thumbnail.jpg", null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    click_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                str(self.post_title.lower()) + str(uuid.uuid4()))
        else:
            pass
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}====>{self.post_title}"


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)
    bookmarked_post = models.ForeignKey(
        Post, on_delete=models.DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}===>{self.bookmarked_post}"


class Report(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)
    reported_post = models.ForeignKey(
        Post, on_delete=models.DO_NOTHING, null=True, blank=True)
    reported_comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}===>{self.reported_post}"
