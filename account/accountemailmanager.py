# accountemailmanager.py
# Single class to generate and send emails
# relating to account management.
# Author: Evan Dempsey
# Last Modified: 15/Oct/2013

from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from models import ActivationKey, RecoveryKey, DeactivationKey

from baseemailmanager import BaseEmailManager
from settings import DEFAULT_REGISTRATION_KEY_VALID_DAYS, DEFAULT_RECOVERY_KEY_VALID_DAYS, \
    DEFAULT_DEACTIVATION_KEY_VALID_DAYS, EMAIL_ADDRESS_ACTIVATE_ACCOUNT, \
    EMAIL_ADDRESS_RECOVER_PASSWORD, EMAIL_ADDRESS_DEACTIVATE_ACCOUNT


class AccountEmailManager(BaseEmailManager):
    def generate_activation_email(self):
        """
        Generate an authorization email.
        """
        # Allow CONSTANT days for activation.
        expiry_date = datetime.today() + timedelta(days=DEFAULT_REGISTRATION_KEY_VALID_DAYS)

        # Generate key and create ActivationKey object.
        activation_key = ActivationKey(user=self.owner,
                                      key=self.generate_hash(),
                                      used=False,
                                      expires=expiry_date)
        activation_key.save()

        # Set up template parameters
        templateFile = "account/email/activation_email.html"
        params = {"username": self.owner.username,
                  "key": activation_key.key}

        # Make EmailMessage instance
        email_subject = "Activate your account."
        email_from = EMAIL_ADDRESS_ACTIVATE_ACCOUNT
        email_body = self.render_HTML_email(templateFile, params)
        email = EmailMessage(email_subject, email_body,
                             email_from, [self.owner.email])

        return email

    def generate_recovery_email(self):
        """
        Generate a password recovery email.
        """
        # Allow CONSTANT days for activation.
        expiry_date = datetime.today() + timedelta(days=DEFAULT_RECOVERY_KEY_VALID_DAYS)

        # Generate key and create ActivationKey object.
        recovery_key = RecoveryKey(user=self.owner,
                                   key=self.generate_hash(),
                                   used=False,
                                   expires=expiry_date)
        recovery_key.save()

        # Set up template parameters
        template_file = "account/email/recovery_email.html"
        params = {"username": self.owner.username,
                  "key": recovery_key.key}

        # Make EmailMessage instance
        email_subject = "Reset your password."
        email_from = EMAIL_ADDRESS_RECOVER_PASSWORD
        email_body = self.render_HTML_email(template_file, params)
        email = EmailMessage(email_subject, email_body,
                             email_from, [self.owner.email])

        return email

    def generate_deactivation_email(self):
        """
        Generate an account deactivation email.
        """
        # Allow CONSTANT days for deactivation.
        expiry_date = datetime.today() + timedelta(days=DEFAULT_DEACTIVATION_KEY_VALID_DAYS)

        # Generate key and create DeactivationKey object.
        deactivation_key = DeactivationKey(user=self.owner,
                                           key=self.generate_hash(),
                                           used=False,
                                           expires=expiry_date)
        deactivation_key.save()

        # Set up template parameters
        template_file = "account/email/deactivation_email.html"
        params = {"username": self.owner.username,
                  "key": deactivation_key.key}

        # Make EmailMessage instance
        email_subject = "Deactivate your account."
        email_from = EMAIL_ADDRESS_DEACTIVATE_ACCOUNT
        email_body = self.render_HTML_email(template_file, params)
        email = EmailMessage(email_subject, email_body,
                             email_from, [self.owner.email])

        return email
