"""Custom login model."""

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)


class MINSUserManager(BaseUserManager):
    """Handle logins."""

    def create_user(self, email, person_type, password=None):
        """User creation."""
        if not email:
            raise ValueError('An email address must be provided')

        now = timezone.now()
        user = self.model(email=email,
                          password=password,
                          is_staff=False,
                          email_verified=False,
                          is_active=True,
                          is_superuser=False,
                          person_type=person_type,
                          last_login=None,
                          date_joined=now,
                          )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, person_type, password=None):
        """Super user creation."""
        user = self.create_user(email=email,
                                person_type=person_type,
                                password=password
                                )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    """This is the class."""

    person_type = models.IntegerField(
        default=1, choices=[(1, 'Individual / Corporate'), (2, 'Broker'),
                            (3, 'Agent'), (4, 'Bank'),
                            (5, 'Insurance Company'),
                            (6, 'Clearing Agent / Consolidator')])
    email = models.EmailField(max_length=200, unique=True)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    password_changed = models.DateTimeField(null=True)
    company_id = models.IntegerField(null=True)
    site = models.ForeignKey(Site, default=1)
    primary = models.BooleanField(default=False)

    objects = MINSUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['person_type']

    def get_short_name(self):
        """Return email."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """To send email."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        """Admin overrides."""

        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'


class AccountVerification(models.Model):
    """Model for Persons details."""

    email = models.EmailField(max_length=200, unique=True)
    verification_code = models.UUIDField()
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'auth_verification'
        verbose_name = 'Verification'
        verbose_name_plural = 'Verifications'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s %s' % (self.email)
