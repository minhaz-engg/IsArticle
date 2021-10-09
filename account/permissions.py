from django.contrib.auth.mixins import AccessMixin

from .models import Institution


class LoginRequiredAndIsRightUserMixin(AccessMixin):
    """Verify that the current user is authenticated and Targetted blog is its author's."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != Institution.objects.get(pk=self.get_object().pk).user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)