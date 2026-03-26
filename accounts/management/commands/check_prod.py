from __future__ import annotations

import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sanity-check production settings/env (Render-friendly)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Exit with non-zero if warnings exist.",
        )

    def handle(self, *args, **options):
        strict = bool(options["strict"])
        warnings: list[str] = []
        errors: list[str] = []

        debug = bool(getattr(settings, "DEBUG", False))
        if debug:
            warnings.append("DEBUG=True (production should use DEBUG=False).")

        allowed_hosts = list(getattr(settings, "ALLOWED_HOSTS", []))
        if not allowed_hosts and not debug:
            errors.append("ALLOWED_HOSTS is empty.")
        if "*" in allowed_hosts and not debug:
            errors.append("ALLOWED_HOSTS contains '*'.")

        csrf_trusted = list(getattr(settings, "CSRF_TRUSTED_ORIGINS", []))
        if not csrf_trusted and not debug:
            warnings.append("CSRF_TRUSTED_ORIGINS is empty (may break POST on custom domains).")

        admin_path = (os.environ.get("ADMIN_PATH") or "").strip()
        if not debug and admin_path and admin_path.rstrip("/") == "admin":
            warnings.append("ADMIN_PATH is set to admin/ (consider a non-guessable path).")

        # Bootstrap envs should be removed after setup.
        if (os.environ.get("BOOTSTRAP_ADMIN_TOKEN") or "").strip():
            warnings.append("BOOTSTRAP_ADMIN_TOKEN is set (remove after creating admin).")
        if os.environ.get("BOOTSTRAP_SUPERUSER") == "True":
            warnings.append("BOOTSTRAP_SUPERUSER=True (set to False/remove after admin is created).")
        if (os.environ.get("BOOTSTRAP_SUPERUSER_PASSWORD") or "").strip():
            warnings.append("BOOTSTRAP_SUPERUSER_PASSWORD is set (remove after admin is created).")

        # Manual payment details (optional but recommended).
        if not (os.environ.get("PAYMENT_CARD_NUMBER") or "").strip():
            warnings.append("PAYMENT_CARD_NUMBER is not set (payment page will show 'not configured').")

        secure_ssl_redirect = getattr(settings, "SECURE_SSL_REDIRECT", False)
        session_cookie_secure = getattr(settings, "SESSION_COOKIE_SECURE", False)
        csrf_cookie_secure = getattr(settings, "CSRF_COOKIE_SECURE", False)
        if not debug:
            if not secure_ssl_redirect:
                warnings.append("SECURE_SSL_REDIRECT=False (recommended True).")
            if not session_cookie_secure:
                warnings.append("SESSION_COOKIE_SECURE=False (recommended True).")
            if not csrf_cookie_secure:
                warnings.append("CSRF_COOKIE_SECURE=False (recommended True).")

        self.stdout.write("check_prod:")
        self.stdout.write(f"  DEBUG={debug}")
        self.stdout.write(f"  ALLOWED_HOSTS={allowed_hosts}")
        self.stdout.write(f"  CSRF_TRUSTED_ORIGINS={csrf_trusted}")

        if errors:
            self.stdout.write(self.style.ERROR("Errors:"))
            for e in errors:
                self.stdout.write(self.style.ERROR(f"  - {e}"))

        if warnings:
            self.stdout.write(self.style.WARNING("Warnings:"))
            for w in warnings:
                self.stdout.write(self.style.WARNING(f"  - {w}"))

        if errors or (strict and warnings):
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS("OK"))
