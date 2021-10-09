from django.contrib import admin

from .models import (Bookmark, Category, CategorySubscribe, CustomizedTag,
                     Post, Report)


# Register your models here.
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Bookmark)
admin.site.register(Report)
admin.site.register(CustomizedTag)
admin.site.register(CategorySubscribe)
