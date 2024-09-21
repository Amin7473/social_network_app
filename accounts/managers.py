from django.contrib.auth.models import (
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to create superuser or user
    """

    def create_superuser(self, email, password):
        if email is None:
            raise ValueError("email")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.username = "Admin"
        user.role = "ADMIN"
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user