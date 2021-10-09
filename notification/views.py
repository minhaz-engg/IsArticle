from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification


# Create your views here.
@login_required
def ShowNOtifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    # seen_notifications = Notification.objects.filter(user=user,is_seen=True).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    # Notification.objects.filter(user=user, is_seen=True).update(is_seen=False)
    context = {
        'notifications': notifications,
        # "seen_notifications": seen_notifications,
        }
    return render(request, 'notification/notification.html', context)

@login_required
def DeleteNotification(request, noti_id):
    user = request.user
    notification = get_object_or_404(Notification, id=noti_id)
    if notification.user == user:
        Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('notification:show-notifications')


def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
        
    context = {
        'count_notifications':count_notifications
        }
    return context

