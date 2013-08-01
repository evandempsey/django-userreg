# accountemailmanager.py
# Single class to generate and send emails
# relating to account management.
# Author: Evan Dempsey
# Last Modified: 01/Aug/2013

from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from models import ActivationKey, RecoveryKey, DeactivationKey

from baseemailmanager import BaseEmailManager
from settings import DEFAULT_REGISTRATION_KEY_VALID_DAYS, DEFAULT_RECOVERY_KEY_VALID_DAYS, \
    DEFAULT_DEACTIVATION_KEY_VALID_DAYS, EMAIL_ADDRESS_ACTIVATE_ACCOUNT, \
    EMAIL_ADDRESS_RECOVER_PASSWORD, EMAIL_ADDRESS_DEACTIVATE_ACCOUNT


class AccountEmailManager(BaseEmailManager):
    def activationEmail(self):
        """
        Generate an authorization email.
        """
        # Allow CONSTANT days for activation.
        expiryDate = datetime.today() + timedelta(days=DEFAULT_REGISTRATION_KEY_VALID_DAYS)

        # Generate key and create ActivationKey object.
        activationKey = ActivationKey(user=self.owner,
                                      key=self.generateHash(),
                                      used=False,
                                      expires=expiryDate)
        activationKey.save()

        # Set up template parameters
        templateFile = "account/email/activation_email.html"
        params = {"username": self.owner.username,
                  "key": activationKey.key}

        # Make EmailMessage instance
        emailSubject = "Activate your account."
        emailFrom = EMAIL_ADDRESS_ACTIVATE_ACCOUNT
        emailBody = self.renderHTMLEmail(templateFile, params)
        email = EmailMessage(emailSubject, emailBody,
                             emailFrom, [self.owner.email])

        return email

    def recoveryEmail(self):
        """
        Generate a password recovery email.
        """
        # Allow CONSTANT days for activation.
        expiryDate = datetime.today() + timedelta(days=DEFAULT_RECOVERY_KEY_VALID_DAYS)

        # Generate key and create ActivationKey object.
        recoveryKey = RecoveryKey(user=self.owner,
                                  key=self.generateHash(),
                                  used=False,
                                  expires=expiryDate)
        recoveryKey.save()

        # Set up template parameters
        templateFile = "account/email/recovery_email.html"
        params = {"username": self.owner.username,
                  "key": recoveryKey.key}

        # Make EmailMessage instance
        emailSubject = "Reset your password."
        emailFrom = EMAIL_ADDRESS_RECOVER_PASSWORD
        emailBody = self.renderHTMLEmail(templateFile, params)
        email = EmailMessage(emailSubject, emailBody,
                             emailFrom, [self.owner.email])

        return email

    def deactivationEmail(self):
        """
        Generate an account deactivation email.
        """
        # Allow CONSTANT days for deactivation.
        expiryDate = datetime.today() + timedelta(days=DEFAULT_DEACTIVATION_KEY_VALID_DAYS)

        # Generate key and create DeactivationKey object.
        deactivationKey = DeactivationKey(user=self.owner,
                                          key=self.generateHash(),
                                          used=False,
                                          expires=expiryDate)
        deactivationKey.save()

        # Set up template parameters
        templateFile = "account/email/deactivation_email.html"
        params = {"username": self.owner.username,
                  "key": deactivationKey.key}

        # Make EmailMessage instance
        emailSubject = "Deactivate your account."
        emailFrom = EMAIL_ADDRESS_DEACTIVATE_ACCOUNT
        emailBody = self.renderHTMLEmail(templateFile, params)
        email = EmailMessage(emailSubject, emailBody,
                             emailFrom, [self.owner.email])

        return email
