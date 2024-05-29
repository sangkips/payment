import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models import JSONField
from django.utils import timezone

# Create your models here.

USERS_ROLES = (
    ("STAFFS", "STAFF"),
    ("USER", "USER"),
    ("ADMIN", "ADMIN")
)

token_type = (
    ("verify_email", 'verify_email'),
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, first_name, email,
                    password=None, is_active=True, is_admin=False,
                    is_staff=False):
        if not username:
            raise ValueError("User must have a username")
        if not first_name:
            raise ValueError("User must have a first name")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must specify password")
        user_obj = self.model(
            username=username,
            first_name=first_name,
            email=email,
            password=password,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save()
        return user_obj

    def create_staff(self, first_name, email, password=None):
        user = self.create_user(
            username=None,
            first_name=first_name,
            email=email,
            password=password,
            is_staff=True
        )

        return user

    def create_superuser(
            self, username, first_name,
            email, password=None
    ):
        user = self.create_user(
            username,
            first_name,
            email,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        blank=True, null=True, unique=True
    )
    first_name = models.CharField(max_length=30)
    referral_code = models.CharField(
        max_length=30,
        blank=True, null=True
    )
    middle_name = models.CharField(
        max_length=30, blank=True, null=True
    )
    last_name = models.CharField(
        max_length=30, null=True, blank=True
    )
   
    username = models.CharField(
        unique=True, max_length=60,
        blank=True, null=True
    )
    email = models.EmailField(unique=True, max_length=60)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(
        blank=True, max_length=500, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    role = models.CharField(
        max_length=50, default="USER",
        choices=USERS_ROLES
    )
    last_updated_password = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email', 'password']
    objects = UserManager()

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.admin
