from django.contrib.auth import get_user_model
from django.db import models

from notification.models import Notification
from post.models import Post

# Create your models here.
User = get_user_model()


class Like(models.Model):
    liked_post = models.ForeignKey(
        Post, on_delete=models.DO_NOTHING, related_name="liked_blog")
    liker_post = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="liker_user")
    created = models.DateTimeField(auto_now_add=True)
    
    # def user_liked_post(sender, instance, *args, **kwargs):
    #     like = instance
    #     post = like.post
    #     sender = like.user
    #     notify = Notification(post=post, sender=sender,
    #                           user=post.user, notification_type=1)
    #     notify.save()

    # def user_unlike_post(sender, instance, *args, **kwargs):
    #     like = instance
    #     post = like.post
    #     sender = like.user

    #     notify = Notification.objects.filter(
    #         post=post, sender=sender, notification_type=1)
    #     notify.delete()

    def __str__(self):
        return f"{self.liker_post}====>{self.liked_post}"
