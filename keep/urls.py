from django.urls import path

from .views import KeepCreate, KeepDelete, KeepDetail, KeepList, KeepUpdate

app_name = "keep"

urlpatterns = [
    path('my-keep-list', KeepList.as_view(), name="keep_list"),
    path('create/', KeepCreate.as_view(), name="keep_create"),
    path('detail/<int:pk>/', KeepDetail.as_view(), name="keep_detail"),
    path('update/<int:pk>/', KeepUpdate.as_view(), name="keep_update"),
    path('delete/<int:pk>/', KeepDelete.as_view(), name="keep_delete"),
]
