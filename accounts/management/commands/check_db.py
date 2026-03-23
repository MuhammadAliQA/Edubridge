from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Print DB config summary and verify a connection with SELECT 1."

    def handle(self, *args, **options):
        connection = connections["default"]
        settings_dict = connection.settings_dict

        engine = settings_dict.get("ENGINE")
        name = settings_dict.get("NAME")
        host = settings_dict.get("HOST")
        port = settings_dict.get("PORT")
        user = settings_dict.get("USER")

        self.stdout.write("default database:")
        self.stdout.write(f"  ENGINE={engine}")
        self.stdout.write(f"  NAME={name}")
        self.stdout.write(f"  HOST={host}")
        self.stdout.write(f"  PORT={port}")
        self.stdout.write(f"  USER={user}")

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
        except OperationalError as exc:
            raise CommandError(f"Database connection failed: {exc}") from exc

        if not row or row[0] != 1:
            raise CommandError(f"Database probe failed (unexpected result): {row}")

        self.stdout.write(self.style.SUCCESS("DB connection OK (SELECT 1)."))

