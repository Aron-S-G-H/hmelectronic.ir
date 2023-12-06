from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, first_name, last_name, phone, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')
        if not password:
            raise ValueError("User must have a password")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(first_name=first_name, last_name=last_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # required for supporting multiple databases
        return user

    def create_superuser(self, first_name, last_name, email, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
