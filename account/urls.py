from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import TemplateView

from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm
from .views import (EducationDelete, InstitutionList, UpdateEducation,
                    account_activate, account_register, apply_author, author_application_accept, author_application_delete, author_application_detail, author_application_list, edit_profile,
                    follow_toggle, user_profile)

app_name = "account"

urlpatterns = [
    path("register/", account_register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html",
         form_class=UserLoginForm), name="login",),
    path("activate/<slug:uidb64>/<slug:token>)/",
         account_activate, name="activate"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="account/password_reset/password_reset_form.html",
         success_url="password_reset_email_confirm", email_template_name="account/password_reset/password_reset_email.html", form_class=PwdResetForm,), name="pwdreset",),
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset/password_reset_confirm.html",
         success_url="password_reset_complete/", form_class=PwdResetConfirmForm,), name="password_reset_confirm",),
    path("password_reset/password_reset_email_confirm/", TemplateView.as_view(
        template_name="account/password_reset/reset_status.html"), name="password_reset_done",),
    path("password_reset_confirm/Mg/password_reset_complete/", TemplateView.as_view(
        template_name="account/password_reset/reset_status.html"), name="password_reset_complete",),

    # dashboard
    path('profile/edit/', edit_profile, name="edit_profile"),
    path('profile/<slug:slug>/', user_profile, name="user_profile"),
    
    #follow
    path('follow/', follow_toggle, name="follow_toggle"),
    path('ins/', InstitutionList.as_view(), name="institution_list"),
    path('ins-edit/<int:pk>/', UpdateEducation.as_view(), name="institution_update"),
    path('ins-delete/<int:pk>/', EducationDelete.as_view(), name="institution_delete"),


    path("author-application-list/", author_application_list, name="author_application_list"),
    path("author-application/", apply_author, name="apply_author"),
    path("author-application-accept/<int:pk>/", author_application_accept, name="author_application_accept"),
    path("author-application-delete/<int:pk>/", author_application_delete, name="author_application_delete"),
    path("author-application-detail/<int:pk>/", author_application_detail, name="author_application_detail"),
]
