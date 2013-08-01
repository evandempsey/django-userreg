from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from settings import DEFAULT_REGISTRATION_KEY_VALID_DAYS
from datetime import datetime, timedelta


class Command(BaseCommand):
    """
    Delete users who have failed to activate their accounts.
    """
    args = ""
    help = "Deletes users who have not activated their accounts."

    def handle(self, *args, **options):
        interval = timedelta(days=DEFAULT_REGISTRATION_KEY_VALID_DAYS)
        cutoff = datetime.today() - interval

        num = 0

        users = User.objects.filter(is_active=False, date_joined__lt=cutoff)
        for user in users:
            user.delete()
            num += 1

        self.stdout.write("Deleted %d inactive users.\n" % num)
