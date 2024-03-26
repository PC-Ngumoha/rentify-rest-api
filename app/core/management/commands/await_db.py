"""
'await_db': command to cause app to wait for DB startup
"""
import time

from psycopg import OperationalError as PsycopgError

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Main command definition."""

    def handle(self, *args, **kwargs):
        """Handles the execution of the command."""
        self.stdout.write('Waiting for Database to start ...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write(
                    'Database not yet available, trying again ...'
                )
                time.sleep(1)
        self.stdout.write(
            self.style.SUCCESS('Database is now available !!!')
        )
