#!/usr/bin/env python

# BaseEmailManager.py
# Base class to generate and send emails
# relating to account management.
# Author: Evan Dempsey
# Last Modified: 01/Aug/2013

from datetime import datetime
from hashlib import sha256
from django.template.loader import get_template
from django.template import Context

from settings import ACCOUNT_KEY_SALT


class BaseEmailManager(object):
    def __init__(self, user):
        """
        Initialize the EmailManager by setting the
        owner to a Django user object.
        """
        self.owner = user

    def renderHTMLEmail(self, template, params):
        """
        Renders a HTML email body given a template
        filename and a dictionary of parameters.
        """
        html = get_template(template)
        context = Context(params)
        body = html.render(context)
        return body

    def generateHash(self):
        """
        Generate a hash from the username
        and the current time.
        """
        stringToHash = self.owner.username + str(datetime.now()) + ACCOUNT_KEY_SALT
        return sha256(stringToHash).hexdigest()
