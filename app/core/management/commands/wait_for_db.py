"""FUNCTION TO WAIT FOR DB TO BE AVAILABLE"""
import time
from django.utils.db import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for the database to be available"""
    def handle(self, *args, **options):
        """Entrypoint for Command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError) as e:
                self.stdout.write(f'Database unavailable: {e}')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database Available!'))