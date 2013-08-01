from django.db import models
from django.contrib.auth.models import User


class ActivationKey(models.Model):
    """
    Key for account activation.
    """
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64)
    used = models.BooleanField()
    expires = models.DateField()


class RecoveryKey(models.Model):
    """
    Key for password recovery.
    """
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64)
    used = models.BooleanField()
    expires = models.DateField()


class DeactivationKey(models.Model):
    """
    Key for account deactivation.
    """
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64)
    used = models.BooleanField()
    expires = models.DateField()


class UserProfile(models.Model):
    """
    UserProfile extends the User model.
    """
    user = models.ForeignKey(User, unique=True)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
