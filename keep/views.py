from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Keep
from .permissions import LoginRequiredandAuthorMixin


# Create your views here.
class KeepList(LoginRequiredMixin, ListView):
    model = Keep

    def get_queryset(self):
        return Keep.objects.filter(author=self.request.user).order_by("-id")
    context_object_name = "keeps"
    ordering = "-id"
    paginate_by = 12
    template_name = "keep/keeplist.html"


class KeepCreate(LoginRequiredMixin, CreateView):
    model = Keep
    template_name = "keep/keepcreate.html"
    success_url = "keep:keep_list"
    fields = ('title', 'detail',)

    def form_valid(self, form):
        post_object = form.save(commit=False)
        post_object.author = self.request.user
        post_object.save()
        return HttpResponseRedirect(reverse('keep:keep_list'))


class KeepDetail(LoginRequiredandAuthorMixin, DetailView):
    model = Keep
    template_name = "keep/keepdetail.html"
    context_object_name = "keep"


class KeepUpdate(LoginRequiredandAuthorMixin, UpdateView):
    model = Keep
    template_name = "keep/keepupdate.html"
    fields = ('title', 'detail',)
    context_object_name = "keep"

    def get_success_url(self, **kwargs):
        return reverse('keep:keep_detail', kwargs={'pk': self.object.pk})


class KeepDelete(LoginRequiredandAuthorMixin, DeleteView):
    model = Keep
    template_name = "keep/keep_confirm_delete.html"
    context_object_name = "keep"

    def get_success_url(self, **kwargs):
        return reverse("keep:keep_list")
