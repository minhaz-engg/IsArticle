from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin

from .models import Post


class LoginAndAuthorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredAndIsAuthorAndIsRightUserMixin(AccessMixin):
    """Verify that the current user is authenticated and Targetted blog is its author's."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_author:
            return self.handle_no_permission()
        if request.user != Post.objects.get(pk=self.get_object().pk).user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def login_and_is__author_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_author,
        # login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
