from django.contrib.auth import get_user_model
from django.db import models

from comment.models import Comment
from post.models import Post

# Create your models here.
User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'),
                          (4, 'Welcome Message'), (5, 'Author Application Accepted'), (6, 'Author Application Denied'))

    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="noti_post", blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.DO_NOTHING, related_name="noti_post", blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_from_user", blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_to_user", blank=True, null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}===>{self.user}==>{self.notification_type}"
