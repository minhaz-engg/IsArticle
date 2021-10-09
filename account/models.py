import uuid
from datetime import date

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy
from django_countries.fields import CountryField
import os
from django.conf import settings

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = f'profile_pictures/user_{instance.email}/profile.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name

class MyUserManager(BaseUserManager):
    """A Custom manager to deal with emails as unique identifier"""

    def _create_user(self, email, password, **extra_fields):
        """Create and Saves a user with a given email and password"""

        if not email:
            raise ValueError("The email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_stuff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)


GENDER_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        ugettext_lazy("staff status"),
        default=False,
        help_text=ugettext_lazy(
            "Designates whether the user can log in this site")
    )
    is_active = models.BooleanField(
        ugettext_lazy("active"),
        default=False,
        help_text=ugettext_lazy(
            "Designates whether this user should br treated as active . Unselect this instade of deleting accounts")
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    headline = models.CharField(max_length=120, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICE, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    country = CountryField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_author = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=user_directory_path, default='default/default.png', blank=True, null=True)
    # -------------
    account_slug = models.SlugField(max_length=264, unique=True, null=False)
    # -------------

    def save(self, *args, **kwargs):
        if not self.account_slug:
            if self.name:
                self.account_slug = slugify(
                    str(self.name.lower()) + str(uuid.uuid4()))
            else:
                self.account_slug = slugify(str(uuid.uuid4()))
        else:
            pass

        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )


class Follow(models.Model):

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='following')

    # def user_follow(self):
    # sender = self.follower
    # user = self.following
    # notification_type = 3
    # notify = Notification(sender=sender, user=user, notification_type=notification_type)
    # notify.save()

    # def user_unfollow(self):
    #     sender = self.follower
    #     user = self.following
    #     notification_type = 3
    #     notify = Notification.objects.filter(sender=sender, user=user, notification_type=notification_type)
    #     notify.delete()

    # def user_follow(sender, instance, *args, **kwargs):
    #     print("follow")
    #     follow = instance
    #     print(follow)
    #     sender = follow.follower
    #     print(sender)
    #     following = follow.following
    #     print(following)

    #     notify = Notification(
    #         sender=sender, user=following, notification_type=3)
    #     notify.save()

    # def user_unfollow(sender, instance, *args, **kwargs):
    #     print("unfollow")
    #     follow = instance
    #     sender = follow.follower
    #     following = follow.following

    #     notify = Notification.objects.filter(
    #         sender=sender, user=following, notification_type=3)
    #     notify.delete()

    def __str__(self):
        return f"{self.follower}===>{self.following}"


class Institution(models.Model):
    degrees = (
        ("Bachelor of Arts: BA", "Bachelor of Arts: BA"),
        ("Bachelor of Business Administration: BBA",
         "Bachelor of Business Administration: BBA"),
        ("Bachelor of Management Studies: BMS",
         "Bachelor of Management Studies: BMS"),
        ("Bachelor of Science: BSc", "Bachelor of Science: BSc"),
        ("Bachelor of Commerce: Bcom", "Bachelor of Commerce: Bcom"),
        ("Bachelor of Computer Applications: BCA",
         "Bachelor of Computer Applications: BCA"),
        ("Bachelor of Fine Arts: BFA", "Bachelor of Fine Arts: BFA"),
        ("Bachelor of Laws: LLB", "Bachelor of Laws: LLB"),
        ("Bachelor of Engineering: BE", "Bachelor of Engineering: BE"),
        ("Bachelor of Technology: BTech", "Bachelor of Technology: BTech"),
        ("Bachelor of Education: BEd", "Bachelor of Education: BEd"),
        ("Bachelor of Medicine, Bachelor of Surgery: MBBS",
         "Bachelor of Medicine, Bachelor of Surgery: MBBS"),
        ("Bachelor of Veterinary Science: BVSc",
         "Bachelor of Veterinary Science: BVSc"),
        ("Bachelor of Architecture: BArch", "Bachelor of Architecture: BArch"),
        ("Master of Arts (M.A.)", "Master of Arts (M.A.)"),
        ("Master of Social Work (MSW)", "Master of Social Work (MSW)"),
        ("Master of Business Administration (M.B.A.)",
         "Master of Business Administration (M.B.A.)"),
        ("Master of Computer Applications (M.C.A.)",
         "Master of Computer Applications (M.C.A.)"),
        ("Master of Engineering (M.Eng.)", "Master of Engineering (M.Eng.)"),
        ("Master of Philosophy (M.Phil.)", "Master of Philosophy (M.Phil.)"),
        ("Master of Science (M.Sc.)", "Master of Science (M.Sc.)"),
        ("Master of Technology (M.Tech.)", "Master of Technology (M.Tech.)"),
        ("Master of Statistics (M.Stat.)", "Master of Statistics (M.Stat.)"),
        ("Master of Laws (LL.M.)", "Master of Laws (LL.M.)"),
        ("Master of Commerce (M.Com.)", "Master of Commerce (M.Com.)"),
        ("Master of Architecture (M.Arch.)", "Master of Architecture (M.Arch.)"),
        ("Master of Veterinary Science (MVSc)",
         "Master of Veterinary Science (MVSc)"),
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=80)
    subject = models.CharField(max_length=60)
    degree = models.CharField(max_length=60, choices=degrees)
    start_year = models.IntegerField(default=date.today().year)
    graduated = models.BooleanField(default=False)
    end_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user}==>{self.name}"

class ApplyAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    accepted = models.BooleanField(default=False)
    deactivated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"