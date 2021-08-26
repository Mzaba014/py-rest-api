from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for Employees"""

    def create_employee(self, email, name, password=None):
        """Creates new employee"""
        if not email:
            raise ValueError('The email value must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name
        )

        user.set_password(password)  # encrypting pass for storage in db
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create new admin user"""
        user = self.create_employee(
            email,
            name,
            password
        )
        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for employees"""

    emp_id = models.AutoField(_('employee id'), primary_key=True)
    email = models.EmailField(_('email'), max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=64)
    last_name = models.CharField(_('last name'), max_length=64)
    hire_date = models.DateField(_("hire date"), default=datetime.date.today)
    birth_date = models.DateField(_('birth date'))
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # get_full_name and get_short_name must be implemented when inheriting from AbstractBaseUser
    def get_full_name(self):
        """Returns employee's full name"""
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """Returns employee's full name"""
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """Return string representation of employee"""
        return self.email
