from django.db import models
from django.contrib.auth.models import User


KEY_TYPE_CHOICES = (('a', 'Activation'),
                    ('r', 'Recovery'),
                    ('d', 'Deactivation'))


class AuthenticationKey(models.Model):
    """
    Key for account activation.
    """
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64)
    key_type = models.CharField(max_length=1, choices=KEY_TYPE_CHOICES)
    used = models.BooleanField()
    expires = models.DateField()
