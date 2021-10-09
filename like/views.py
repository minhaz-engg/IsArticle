from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from notification.models import Notification
from post.models import Post

from .models import Like

try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.


@login_required
@require_POST
def post_like(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)

        already_liked = Like.objects.filter(liked_post=post, liker_post=user)
        if not already_liked:
            liked_post = Like(liked_post=post, liker_post=user)
            liked_post.save()
            message = 'liked'

            if not user == post.user:
                sender = user
                user = post.user
                post = post
                notification_type = 1
                notify = Notification(
                    sender=sender, post=post, user=user, notification_type=notification_type)
                notify.save()

        else:
            already_liked.delete()
            message = 'unliked'

            if not user == post.user:
                sender = user
                user = post.user
                notification_type = 1
                notify = Notification.objects.filter(
                    sender=sender, post=post, user=user, notification_type=notification_type)
                notify.delete()

    total_likes = Like.objects.filter(liked_post=post).count()

    ctx = {'likes_count': total_likes, 'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
