from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                        PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new user in the database"""
        if not email:
            raise ValueError("User must have an email address. ")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        This function creates a new super user to the system.
        """
        if not email:
            raise ValueError("Super suer must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
            is_superuser=True,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user module that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    # dob = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """
    Model for the tag.
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return self.name
