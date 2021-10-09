import json
import math

from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView

from notification.models import Notification
from scientific_application.settings import EMAIL_HOST_USER

from .forms import AuthorApplicationForm, EditProfileForm, InstitutionForm, RegistrationForm
from .models import ApplyAuthor, Follow, Institution
from .permissions import LoginRequiredAndIsRightUserMixin
from .tokens import account_activation_token

# Create your views here.
User = get_user_model()


def account_register(request):
    if request.user.is_authenticated:
        return redirect("post:post_list")
    if request.method == "POST":
        registerForm = RegistrationForm(request.POST, request.FILES)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.image = registerForm.cleaned_data.get('image')
            user.country = registerForm.cleaned_data["country"]
            user.name = registerForm.cleaned_data["name"]
            user.gender = registerForm.cleaned_data["gender"]

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            # user.email_user(subject=subject, message=message)
            send_mail(subject,message, EMAIL_HOST_USER, [user.email], fail_silently = False)
            return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        
        # send welcome notification
        notification_type = 4
        text_preview = "Welcome to Scienctific Article Application"
        notify = Notification(
            user=user, notification_type=notification_type, text_preview=text_preview)
        notify.save()

        return redirect("post:post_list")
    else:
        return render(request, "account/registration/activation_invalid.html")


def user_profile(request, slug):
    user = get_object_or_404(User, account_slug=slug)
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    educations = Institution.objects.filter(user=user).order_by("-id")

    if request.user == user:
        profile_completion = 100

        minus_number = (100/9)

        if user.birthday == None:
            profile_completion -= minus_number
        if user.headline == None:
            profile_completion -= minus_number
        if user.gender == None:
            profile_completion -= minus_number
        if user.country == "":
            profile_completion -= minus_number
        if user.description == "":
            profile_completion -= minus_number
        if user.name == None:
            profile_completion -= minus_number

        profile_completion = math.floor(profile_completion)

        if request.method == "POST":
            education_form = InstitutionForm(request.POST)
            if education_form.is_valid():
                education = education_form.save(commit=False)
                education.user = request.user
                education.save()
                return HttpResponseRedirect(reverse('account:user_profile', kwargs={'slug': user.account_slug}))
        else:
            education_form = InstitutionForm()

        context = {
            'profile': user,
            'profile_completion': profile_completion,
            'following_count': following_count,
            'followers_count': followers_count,
            'educations': educations,
            "education_form": education_form,
        }
    else:
        if request.user.is_authenticated:
            already_followed = Follow.objects.filter(
                following=user, follower=request.user).exists()
            context = {
                'profile': user,
                'already_followed': already_followed,
                'following_count': following_count,
                'followers_count': followers_count,
                'educations': educations,
            }
        else:
            context = {
                'profile': user,
                'following_count': following_count,
                'followers_count': followers_count,
                'educations': educations,
            }
    return render(request, 'account/profile/profile.html', context)

# @login_required
# def institution_list(request):
#     user = request.user
#     institutions = Institution.objects.filter(user=user).order_by("-id")
#     context = {
#         'educations': institutions,
#     }
#     return render(request, 'account/ins_list.html', context)


class InstitutionList(ListView):
    # queryset = Institution.objects.filter(user=request.user).order_by("-id")
    def get_queryset(self):
        queryset = Institution.objects.filter(
            user=self.request.user).order_by("-id")
        return queryset
    template_name = 'account/ins_list.html'
    context_object_name = "educations"


class UpdateEducation(LoginRequiredAndIsRightUserMixin, UpdateView):
    model = Institution
    fields = ("name", "subject", "degree", "start_year",
              "graduated", "end_year", "description")
    template_name = 'account/update_ins.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('account:institution_list')


class EducationDelete(LoginRequiredAndIsRightUserMixin, DeleteView):
    model = Institution
    template_name = "account/ins_confirm_delete.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('account:institution_list')


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:user_profile', kwargs={'slug': user.account_slug}))
    else:
        form = EditProfileForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'account/profile/edit-profile.html', context)


@login_required
def follow_toggle(request):
    if request.method == "POST":
        follower_user = request.user
        pk = request.POST.get('pk', None)
        following_user = get_object_or_404(User, pk=pk)
        if not follower_user == following_user:
            already_followed = Follow.objects.filter(
                following=following_user, follower=follower_user)
            if not already_followed:

                follow = Follow(following=following_user,
                                follower=follower_user)
                follow.save()
                message = "followed"

                sender = follower_user
                user = following_user
                notification_type = 3
                notify = Notification(
                    sender=sender, user=user, notification_type=notification_type)
                notify.save()

            else:

                already_followed.delete()
                message = "unfollowed"

                sender = follower_user
                user = following_user
                notification_type = 3
                notify = Notification.objects.filter(
                    sender=sender, user=user, notification_type=notification_type)
                notify.delete()

            context = {
                "message": message,
            }
            return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            pass


@login_required
def apply_author(request):
    if request.user.is_author:
        return redirect("post:post_list")
    else:
        form = AuthorApplicationForm()
        if request.method == "POST":
            form = AuthorApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.user= request.user
                application.save()
                return HttpResponseRedirect(reverse('account:user_profile', kwargs={'slug': request.user.account_slug}))
        context = {
            'form': form
        }
        return render(request, 'account/author_apply.html', context=context)

@login_required
def author_application_list(request):
    if not request.user.is_superuser:
        print("hello not admin")
        return redirect("post:post_list")
    else:
        application_list = ApplyAuthor.objects.filter(accepted=False).filter(deactivated=False).order_by("-id")
        # print(application_list)
        context = {
            "application_list": application_list,
        }
        return render(request, 'account/author_application_list.html', context=context)

@login_required
def author_application_accept(request, pk):
    if not request.user.is_superuser:
        print("hello not admin")
        return redirect("post:post_list")
    else:

        application = get_object_or_404(ApplyAuthor, pk=pk)
        
        application.accepted = True
        application.save()

        app_user = application.user
        app_user.is_author = True
        app_user.save()

        if not request.user == application.user:
            # sender = user
            user = application.user
            # application = application
            notification_type = 5
            notify = Notification(user=user, notification_type=notification_type)
            notify.save()
        
        return redirect("account:author_application_list")

@login_required
def author_application_delete(request, pk):
    if not request.user.is_superuser:
        print("hello not admin")
        return redirect("post:post_list")
    else:
        print(pk)

        application = get_object_or_404(ApplyAuthor, pk=pk)

        application.deactivated = True
        application.save()

        if not request.user == application.user:
            # sender = user
            user = application.user
            # application = application
            notification_type = 6
            notify = Notification(user=user, notification_type=notification_type)
            notify.save()
        
        
        return redirect("account:author_application_list")

@login_required
def author_application_detail(request, pk):
    if not request.user.is_superuser:
        print("hello not admin")
        return redirect("post:post_list")
    else:
        
        application = get_object_or_404(ApplyAuthor, pk=pk)

        context = {
            "application": application
        }
        return render(request, 'account/application_detail.html', context=context)
