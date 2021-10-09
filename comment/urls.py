from django.urls import path

from comment.views import all_comment_load, delete_comment

app_name = "comment"

urlpatterns = [
    path('load-comment/<int:pk>/', all_comment_load, name="load_comment"),
    path('delete-comment/<int:pk>/', delete_comment, name="delete_comment"),
]
