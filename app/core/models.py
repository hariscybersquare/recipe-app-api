from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                        PermissionsMixin


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
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
