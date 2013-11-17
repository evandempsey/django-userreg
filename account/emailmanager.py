# emailmanager.py
# Single class to generate and send emails
# relating to account management.
# Author: Evan Dempsey
# Last Modified: 17/Nov/2013

from datetime import datetime
from datetime import timedelta
from hashlib import sha256
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

from models import AuthenticationKey
from settings import DEFAULT_REGISTRATION_KEY_VALID_DAYS
from settings import DEFAULT_RECOVERY_KEY_VALID_DAYS
from settings import DEFAULT_DEACTIVATION_KEY_VALID_DAYS
from settings import EMAIL_ADDRESS_ACTIVATE_ACCOUNT
from settings import EMAIL_ADDRESS_RECOVER_PASSWORD
from settings import EMAIL_ADDRESS_DEACTIVATE_ACCOUNT
from settings import ACCOUNT_KEY_SALT


class EmailManager(object):

    def __init__(self, user):
        """
        Initialize the EmailManager by setting the
        owner to a Django user object.
        """
        self.owner = user

    def render_HTML_email(self, template, params):
        """
        Renders a HTML email body given a template
        filename and a dictionary of parameters.
        """
        html = get_template(template)
        context = Context(params)
        return html.render(context)

    def generate_hash(self):
        """
        Generate a hash from the username
        and the current time.
        """
        string_to_hash = self.owner.username + str(datetime.now()) + ACCOUNT_KEY_SALT
        return sha256(string_to_hash).hexdigest()

    def generate_activation_email(self):
        """
        Generate an authorization email.
        """
        # Allow CONSTANT days for activation.
        expiry_date = datetime.today() + timedelta(days=DEFAULT_REGISTRATION_KEY_VALID_DAYS)

        # Generate key and create ActivationKey object.
        activation_key = AuthenticationKey(user=self.owner,
                                      key=self.generate_hash(),
                                      type='a',
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
        recovery_key = AuthenticationKey(user=self.owner,
                                   key=self.generate_hash(),
                                   type='r',
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
        deactivation_key = AuthenticationKey(user=self.owner,
                                           key=self.generate_hash(),
                                           type='d',
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
