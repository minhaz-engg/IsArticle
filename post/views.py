import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.paginator import Paginator
from django.http.response import (HttpResponse, HttpResponseRedirect,
                                  JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from taggit.models import Tag

from account.models import Follow
from comment.forms import CommentForm
from comment.models import Comment
from like.models import Like
from notification.models import Notification

from .models import Bookmark, Category, CategorySubscribe, Post
from .permissions import (LoginAndAuthorRequiredMixin,
                          LoginRequiredAndIsAuthorAndIsRightUserMixin,
                          login_and_is__author_required)

# Create your views here.
User = get_user_model()

# class PostList(ListView):
#     context_object_name = 'posts'
#     ordering = ("-id", )
#     paginate_by = 7
#     model = Post
#     template_name = 'post/post_list.html'

#     def get_context_data(self, **kwargs):
#         context = super(PostList, self).get_context_data(**kwargs)
#         context.update({
#             'categories': Category.objects.all(),
#         })
#         return context


def PostList(request):
    if request.user.is_authenticated:
        subscribed_categories = CategorySubscribe.objects.filter(
            subscriber=request.user)
        my_category_ids = []

        for i in subscribed_categories:
            my_category_ids.append(i.subscribed_category.id)

        following_list = Follow.objects.filter(follower=request.user)

        following_posts = Post.objects.filter(
            user__in=following_list.values_list('following'))
        subscribed_posts = Post.objects.filter(
            is_active=True).filter(category_id__in=my_category_ids)

        posts = following_posts.union(subscribed_posts).order_by("-id")

        # posts = Post.objects.filter(is_active=True).filter(category_id__in=my_category_ids).order_by("-id")
        latest_post = posts.first()
        paginator = Paginator(posts, 7)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        top_6_read_post = Post.objects.filter(
            is_active=True).order_by("-click_count")[:6]

        # most_read_post = Post.objects.filter()
        all_categories = Category.objects.all()

        context = {
            'posts': posts,
            'all_categories': all_categories,
            'top_6_read_post': top_6_read_post,
            'latest_post': latest_post,
            'subscribed_categories': subscribed_categories,
        }
        return render(request, 'post/post_list.html', context)
    else:
        posts = Post.objects.filter(is_active=True).order_by("-id")
        latest_post = posts.first()
        paginator = Paginator(posts, 7)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        top_6_read_post = Post.objects.filter(
            is_active=True).order_by("-click_count")[:6]

        # most_read_post = Post.objects.filter()
        all_categories = Category.objects.all()

        context = {
            'posts': posts,
            'all_categories': all_categories,
            'top_6_read_post': top_6_read_post,
            'latest_post': latest_post,
        }
        return render(request, 'post/post_list.html', context)


@login_required
def subscribe_category(request):
    if request.method == "POST":
        user = request.user
        pk = request.POST.get('pk', None)
        subscribed_category = get_object_or_404(Category, pk=pk)

        already_subscribed = CategorySubscribe.objects.filter(
            subscriber=user, subscribed_category=subscribed_category)
        if not already_subscribed:
            subscribe = CategorySubscribe(
                subscriber=user, subscribed_category=subscribed_category)
            subscribe.save()
            message = 'subscribed'
        else:
            already_subscribed.delete()
            message = 'unsubscribed'
    context = {
        "message": message,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def category_list(request):
    all_category = Category.objects.all()

    my_subscribed_category = CategorySubscribe.objects.filter(
        subscriber=request.user)
    my_subscribed_category_ids = []

    for i in my_subscribed_category:
        my_subscribed_category_ids.append(i.subscribed_category.id)

    context = {
        "my_subscribed_category_ids": my_subscribed_category_ids,
        "all_category": all_category,
    }
    return render(request, 'post/category_list.html', context)


# @login_required
# def category_list(request):
#     all_categories = Category.objects.all()

#     #subscribed category
#     subscribed_categories = CategorySubscribe.objects.filter(subscriber=request.user)
#     subscribed_category_list = []
#     for i in subscribed_categories:
#         abc= Category.objects.filter(name=i.subscribed_category.name)
#         subscribed_category_list.append(abc)
#     print(subscribed_category_list)


#     not_subscribed_category_list = []
#     for i in all_categories:
#         print(i)
#         if i in subscribed_category_list:
#             pass
#         else:
#             not_subscribed_category_list.append(i)
#     # not_subscribed_categories = Category.objects.exclude(id__in=subscribed_category_list)

#     print(not_subscribed_category_list)

#     # print(not_subscribed_categories)

    # context = {
    #     'subscribed_categories':subscribed_categories,
    #     # 'categories': categories,
    # }
    # return render(request, 'post/category_list.html', context)

# def category_toggle(request,pk):


class CreatePost(LoginAndAuthorRequiredMixin, CreateView):
    model = Post
    template_name = 'post/create_post.html'
    fields = ('post_title', 'category', 'tags', 'post_content', 'thumbnail',)
    success_url = "post:my_blogs"

    def form_valid(self, form):
        post_object = form.save(commit=False)
        post_object.user = self.request.user

        post_object.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('post:my_blogs'))


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.is_active:
        post.click_count += 1
        post.save()

        comment_list = Comment.objects.filter(target_post=post).order_by("-id")
        total_comments = comment_list.count()
        paginator = Paginator(comment_list, 5)
        page_number = request.GET.get('page')

        comments_pagination = []
        if not page_number == None:
            for i in range(1, int(page_number)+1):
                comments_pagination.append(paginator.get_page(i))

        comment_list = paginator.get_page(page_number)
        if comment_list:
            last_pagination_comment_id = comment_list[0].id
        

        comments = []
        for i in comments_pagination:
            for j in i:
                comments.append(j)

        recommended_posts = Post.objects.filter(
            category=post.category).filter(is_active=True).order_by("-id")[:6]

        if request.user.is_authenticated:
            comment_form = CommentForm()
            already_liked = Like.objects.filter(
                liked_post=post, liker_post=request.user)
            already_bookmarked = Bookmark.objects.filter(
                bookmarked_post=post, user=request.user)

            if already_bookmarked:
                bookmarked = True
            else:
                bookmarked = False

            if already_liked:
                liked = True
            else:
                liked = False

            if request.method == 'POST':
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.user = request.user
                    comment.target_post = post
                    comment.save()
                    
                    if not comment.user == post.user:
                        sender = comment.user
                        user = post.user
                        post = post
                        comment = comment
                        notification_type = 2
                        notify = Notification(
                            sender=sender, post=post,comment=comment, user=user, notification_type=notification_type)
                        notify.save()
                    
                    
                    return HttpResponseRedirect(f'/details/{slug}#comment-part')
                    # return HttpResponseRedirect(reverse('post:post_details', kwargs={'slug': slug}))
            
            if comment_list:
                context = {'post': post, 'liked': liked, 'comment_form': comment_form, "total_comments": total_comments, "last_pagination_comment_id": last_pagination_comment_id,
                       "comment_list": comment_list, "comments": comments, 'bookmarked': bookmarked, "recommended_posts": recommended_posts}
            else:
                context = {'post': post, 'liked': liked, 'comment_form': comment_form, "total_comments": total_comments,
                       "comment_list": comment_list, "comments": comments, 'bookmarked': bookmarked, "recommended_posts": recommended_posts}
        else:
            if comment_list:
                context = {'post': post, "comment_list": comment_list, "comments": comments, "total_comments": total_comments, "last_pagination_comment_id": last_pagination_comment_id,
                       "recommended_posts": recommended_posts}
            else:
                context = {'post': post, "comment_list": comment_list, "comments": comments, "total_comments": total_comments,
                       "recommended_posts": recommended_posts}
        return render(request, 'post/post_details.html', context)
    else:
        return redirect("post:post_list")


class UpdatePost(LoginRequiredAndIsAuthorAndIsRightUserMixin, UpdateView):
    model = Post
    fields = ('post_title', 'category', 'tags', 'post_content', 'thumbnail',)
    template_name = 'post/update_post.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post:post_details', kwargs={'slug': self.object.slug})


@login_required
def MyPosts(request):
    if request.user.is_author:
        my_posts = Post.objects.filter(user=request.user).order_by("-id")
        paginator = Paginator(my_posts, 7)
        page_number = request.GET.get('page')
        my_posts = paginator.get_page(page_number)
        context = {
            'posts': my_posts,
        }
        return render(request, 'post/my_posts.html', context)
    else:
        return redirect("post:post_list")


@login_required
def deactivate_blog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user == post.user and post.user.is_author == True:
        if post.is_active == True:
            post.is_active = False
            post.save()
        else:
            post.is_active = True
            post.save()
    else:
        return redirect("post:post_list")
    return redirect("post:my_blogs")


class BlogDelete(LoginRequiredAndIsAuthorAndIsRightUserMixin, DeleteView):
    model = Post
    template_name = "post/post_confirm_delete.html"

    def get_success_url(self, **kwargs):
        return reverse("post:my_blogs")


@login_required
def bookmark(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)

        already_bookmarked = Bookmark.objects.filter(
            bookmarked_post=post, user=user)
        if not already_bookmarked:
            bookmark_post = Bookmark(bookmarked_post=post, user=user)
            bookmark_post.save()
            message = 'bookmarked'
        else:
            already_bookmarked.delete()
            message = 'unbookmarked'
    ctx = {'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
def bookmark_list(request):
    all_bookmarked = Bookmark.objects.filter(user=request.user)

    paginator = Paginator(all_bookmarked, 5)
    page_number = request.GET.get('page')
    all_bookmarked = paginator.get_page(page_number)

    # all_bookmarked_post_list = []

    # for bookmark in all_bookmarked:
    #     all_bookmarked_post_list.append(bookmark.bookmarked_post)

    context = {
        "posts": all_bookmarked,
    }

    return render(request, 'post/my_bookmark_post.html', context)


# @login_required
# def bookmark_delete(request):
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('productid'))
#         basket.delete(product=product_id)

#         basketqty = basket.__len__()
#         baskettotal = basket.get_total_price()
#         response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
#         return response


def category_based_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)

    category_posts = Post.objects.filter(
        category=category).filter(is_active=True).order_by("-id")

    # posts = Post.objects.filter(
    #     category__in=Category.objects.get(slug=category_slug)
    # )

    paginator = Paginator(category_posts, 7)
    page_number = request.GET.get('page')
    category_posts = paginator.get_page(page_number)

    if request.user.is_authenticated:
        already_subscribed = CategorySubscribe.objects.filter(
            subscriber=request.user, subscribed_category=category)
        context = {
            "category": category,
            'posts': category_posts,
            "already_subscribed": already_subscribed,
        }
    else:
        context = {
            "category": category,
            'posts': category_posts,
        }
    return render(request, "post/category_posts.html", context)


def tag_based_list(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = Post.objects.filter(tags=tag).filter(
        is_active=True).order_by("-id")

    paginator = Paginator(posts, 7)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'post/tag_posts.html', context)


def writters_posts(request, slug):
    writer = get_object_or_404(User, account_slug=slug)
    if writer.is_author:
        writters_posts = Post.objects.filter(
            is_active=True).filter(user=writer).order_by("-id")

        paginator = Paginator(writters_posts, 7)
        page_number = request.GET.get('page')
        writters_posts = paginator.get_page(page_number)

        context = {
            'writer': writer,
            'posts': writters_posts,
        }
        return render(request, 'post/writter_posts.html', context)
    else:
        return redirect("account:user_profile", slug=writer.account_slug)
