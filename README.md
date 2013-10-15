django-userreg
==============

An account registration and management app for Django.

Installation is simple. Just add 'account' to the INSTALLED_APPS tuple in your settings.py and provide your own values for the following variables.

# Add these variables to your settings.py

ACCOUNT_KEY_SALT = "abcd123"
DEFAULT_REGISTRATION_KEY_VALID_DAYS = 30
DEFAULT_RECOVERY_KEY_VALID_DAYS = 2
DEFAULT_DEACTIVATION_KEY_VALID_DAYS = 2
EMAIL_ADDRESS_ACTIVATE_ACCOUNT = "activate-account@test.com"
EMAIL_ADDRESS_RECOVER_PASSWORD = "recover-password@test.com"
EMAIL_ADDRESS_DEACTIVATE_ACCOUNT = "deactivate-account@test.com"

SITE_URL = "/"
LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/home/"
LOGOUT_REDIRECT_URL = "/"

Then create your own versions of the files in the templates directory.

The app extends manage.py with a new command, purgeinactiveusers, that deletes users that signed up for accounts but never activated them. It deletes all users whose accounts are in an inactive state and who signed up more than DEFAULT_REGISTRATION_KEY_VALID_DAYS days ago. Usage is as follows:
python manage.py purgeinactiveusers

You might want to set this to run as a cron job.

