import time
from django.db import connections   # to test if db connection is available
from django.db.utils import OperationalError  # error to be thrown by django
# class to build on in order to create custom commands
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause command until database is available"""

    # this function is ran whenever the management command is ran
    def handle(self, *args, **options):
        """ *args, **options - pass in custom args into this function"""
        self.stdout.write('Waiting for database...')   # output msg to screen
        db_conn = None
        while not db_conn:  # falsy
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
