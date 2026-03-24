from __future__ import annotations

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from env vars (safe for Render Free without shell)."

    def handle(self, *args, **options):
        enabled = (os.environ.get("BOOTSTRAP_SUPERUSER", "False") == "True")
        if not enabled:
            self.stdout.write("BOOTSTRAP_SUPERUSER is not True; skipping.")
            return

        username = (os.environ.get("BOOTSTRAP_SUPERUSER_USERNAME") or "").strip()
        email = (os.environ.get("BOOTSTRAP_SUPERUSER_EMAIL") or "").strip()
        password = os.environ.get("BOOTSTRAP_SUPERUSER_PASSWORD") or ""

        if not username or not email or not password:
            self.stdout.write(
                "Missing env vars; set BOOTSTRAP_SUPERUSER_USERNAME/EMAIL/PASSWORD. Skipping."
            )
            return

        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("A superuser already exists; skipping.")
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        if created:
            self.stdout.write(f"User created: {username}")
        else:
            self.stdout.write(f"User exists: {username} (will be promoted to superuser)")

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(update_fields=["email", "is_staff", "is_superuser", "password"])

        self.stdout.write(self.style.SUCCESS("Superuser ready (created/promoted)."))
