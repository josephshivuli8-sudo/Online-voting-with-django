from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# 1. Custom Manager Class
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        # 1. Normalize email
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        # 2. Create the user instance
        user = self.model(email=email, **extra_fields)

        # 3. Hash and set password
        user.set_password(password)  # Use set_password instead of make_password directly

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        # Set default user type for regular users (Voter)
        extra_fields.setdefault("user_type", "2")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # Set user type for superuser (Admin)
        extra_fields.setdefault("user_type", "1")

        # Validation checks (Crucial Fix)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


# 2. Custom User Model
class CustomUser(AbstractUser):
    # Use CharField for user_type in model, but map to integer choices
    USER_TYPE_CHOICES = (
        ("1", "Admin"),
        ("2", "Voter")
    )

    # Inherits first_name, last_name, is_staff, is_superuser, etc., from AbstractUser

    username = None  # Removes the username field

    email = models.EmailField(_("email address"), unique=True)

    # Use CharField with max_length 1 to store the choice key
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default="2")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # REQUIRED_FIELDS are only for createsuperuser (email is handled by USERNAME_FIELD)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    # Corrected __str__ method (Uses standard inherited fields)
    def __str__(self):
        # Display the user's name or fallback to email
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email
