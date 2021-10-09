from django.urls import path

from .views import post_like

app_name = "like"
urlpatterns = [
    path('like-post/', post_like, name="post_like")
]
