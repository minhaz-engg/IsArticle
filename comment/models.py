from django.contrib.auth import get_user_model
from django.db import models

from post.models import Post

# Create your models here.
User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='user_comment')
    target_post = models.ForeignKey(
        Post, on_delete=models.DO_NOTHING, related_name='post_comment')
    comment = models.CharField(
        max_length=280, help_text="maximum 280 character")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}===>{self.target_post}"
