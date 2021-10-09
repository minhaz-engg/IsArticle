from django.urls import path

from .views import (BlogDelete, CreatePost, MyPosts, PostList, UpdatePost,
                    bookmark, bookmark_list, category_based_list,
                    category_list, deactivate_blog, post_details,
                    subscribe_category, tag_based_list, writters_posts)

app_name = "post"

urlpatterns = [
    path('', PostList, name='post_list'),
    path('details/<slug:slug>', post_details, name='post_details'),
    path('write/', CreatePost.as_view(), name='create_post'),
    path('edit/<pk>/', UpdatePost.as_view(), name='edit_blog'),
    path('my-blogs/', MyPosts, name='my_blogs'),
    path('deactivate-blog/<pk>/', deactivate_blog, name="deactivate_blog"),
    path('blog-delete/<int:pk>/', BlogDelete.as_view(), name="blog_delete"),

    path('add-bookmark/', bookmark, name="bookmark"),
    path('bookmark-list/', bookmark_list, name="bookmark_list"),


    path('category/<slug:category_slug>/',
         category_based_list, name='category_based_list'),
    path('tag/<slug:slug>/', tag_based_list, name="tag_based_list"),

    path("writter-posts/<slug:slug>/", writters_posts, name="writters_posts"),
    path('subscribe-category/', subscribe_category, name="subscribe_category"),
    path('category-list/', category_list, name="category_list"),
]
