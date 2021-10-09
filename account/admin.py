from django.contrib import admin

from .models import ApplyAuthor, Follow, Institution, User

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Institution)
admin.site.register(ApplyAuthor)
