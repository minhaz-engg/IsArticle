from django.urls import path

from .views import DeleteNotification, ShowNOtifications

app_name = "notification"
urlpatterns = [
   	path('', ShowNOtifications, name='show-notifications'),
   	path('<noti_id>/delete', DeleteNotification, name='delete-notification'),
]