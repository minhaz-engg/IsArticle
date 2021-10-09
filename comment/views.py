from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from notification.models import Notification
from post.models import Post

from .models import Comment

# Create your views here.
User = get_user_model()


def all_comment_load(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_list = post.post_comment.all().order_by("-id")

    paginator = Paginator(comment_list, 6)
    page_number = request.GET.get('page')
    comment_list = paginator.get_page(page_number)

    if(comment_list.has_previous()):
        print("Previous page YES. ", comment_list.previous_page_number())
    else:
        print("Previous page No")

    if(comment_list.has_next()):
        print("Next page YES. ", comment_list.next_page_number())
    else:
        print("Previous page no")

    # if(comment_list.has_previous()):
    #     page_previous = True

    total_page_number = comment_list.paginator.num_pages
    current_page = comment_list.number

    data = serializers.serialize('json', comment_list)
    context = {
        'data': data,
        'total_page_number': total_page_number,
        "current_page": current_page
    }
    return JsonResponse(context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.target_post
    if comment.user == request.user:
        if not comment.user == post.user:
            sender = comment.user
            user = post.user
            post = post
            comment = comment
            notification_type = 2
            notify = Notification.objects.filter(
                sender=sender, post=post,comment=comment, user=user, notification_type=notification_type)
            notify.delete()
            
        comment.delete()
        
        
        return HttpResponseRedirect(f'/details/{post.slug}#comment-part')
        # return redirect('post:post_details', slug=post.slug)
    else:
        return HttpResponseRedirect(f'/details/{post.slug}#comment-part')
        # return redirect('post:post_details', slug=post.slug)
