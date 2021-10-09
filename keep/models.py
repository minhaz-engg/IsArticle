from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Keep(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(
        max_length=70, help_text="Max Length 80 Character")
    detail = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}===>{self.title}"
