from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import MentorProfile


@dataclass(frozen=True)
class SeedMentor:
    first_name: str
    last_name: str
    email: str
    yonalish: str
    viloyat: str
    ball: float | None
    bio_lines: list[str]


MENTORS: list[SeedMentor] = [
    SeedMentor(
        first_name="Saidalo",
        last_name="Ibrohimov",
        email="saidaloibrokhimov04@gmail.com",
        yonalish="ingliz_tili",  # Admission
        viloyat="toshkent_sh",
        ball=1550,
        bio_lines=[
            "SAT 1550 (750 EBRW)",
            "IELTS 7.0 (2024)",
            "Research assistant of prof. Bekhzod Khoshimov",
            "Founder of Inquirum",
            "Founder of Flux Esports",
            "Internship at Korzinka",
            "LaunchX '25 finalist",
            "School President",
            "Football Enthusiast",
        ],
    ),
    SeedMentor(
        first_name="Sunnat",
        last_name="Toirov",
        email="toirovsunnatjon01@gmail.com",
        yonalish="ielts",
        viloyat="toshkent_sh",
        ball=7.0,
        bio_lines=[
            "IELTS 7.0",
            "Imkon scholar winner",
            "Accepted to PIF",
            "600+ hours hospital working experience",
            "Bio School program",
            "Biology researcher",
        ],
    ),
    SeedMentor(
        first_name="Roziyabonu",
        last_name="Ismailova",
        email="ismailovabonusha@gmail.com",
        yonalish="ielts",
        viloyat="toshkent_sh",
        ball=7.5,
        bio_lines=[
            "IELTS 7.5",
            "Student of PIF",
            "Mentor at Financopedia business case",
            "Ibrat debate 3rd place (regional)",
            "Municipial Olympiad #1",
            "President of eco club at school",
        ],
    ),
    SeedMentor(
        first_name="Shakhina",
        last_name="Kiyomidinova",
        email="kiyomidinovashakhina@gmail.com",
        yonalish="ielts",
        viloyat="toshkent_sh",
        ball=7.5,
        bio_lines=[
            "IELTS 7.5",
            "Student of PIF",
            "Summer Camp IT for English '25",
            "Volunteered at Bienalle in Bukhara",
            "English olympiad 2nd in city",
            "Literature olympiad 1st in city",
        ],
    ),
]


class Command(BaseCommand):
    help = "Seed a few mentor profiles (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--approve",
            action="store_true",
            help="Mark mentors as approved (tasdiqlangan=True).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        approve = bool(options["approve"])

        created_users = 0
        created_profiles = 0
        updated_profiles = 0

        for mentor in MENTORS:
            username_base = mentor.email.split("@", 1)[0]
            username = username_base
            suffix = 1
            while User.objects.filter(username=username).exclude(email=mentor.email).exists():
                suffix += 1
                username = f"{username_base}{suffix}"

            user, user_created = User.objects.get_or_create(
                email=mentor.email,
                defaults={"username": username, "first_name": mentor.first_name, "last_name": mentor.last_name},
            )
            if user_created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
                created_users += 1
            else:
                changed = False
                if mentor.first_name and user.first_name != mentor.first_name:
                    user.first_name = mentor.first_name
                    changed = True
                if mentor.last_name and user.last_name != mentor.last_name:
                    user.last_name = mentor.last_name
                    changed = True
                if changed:
                    user.save(update_fields=["first_name", "last_name"])

            haqida = "\n".join(f"• {line}" for line in mentor.bio_lines)

            profile, profile_created = MentorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "viloyat": mentor.viloyat,
                    "yonalish": mentor.yonalish,
                    "tajriba_yil": 1,
                    "haqida": haqida,
                    "ball": mentor.ball,
                    "tajriba": "Tajriba haqida qisqacha.",
                    "metodologiya": "Metodologiya haqida qisqacha.",
                    "muvaffaqiyat": "Muvaffaqiyatlar haqida qisqacha.",
                    "vaqt": "Haftada 3 marta, 1.5 soatdan (kelishiladi).",
                    "maqsad": "EduBridge orqali ko'proq o'quvchiga yordam berish.",
                    "tasdiqlangan": approve,
                },
            )
            if profile_created:
                created_profiles += 1
            else:
                fields_to_update: list[str] = []
                for field, value in [
                    ("viloyat", mentor.viloyat),
                    ("yonalish", mentor.yonalish),
                    ("haqida", haqida),
                    ("ball", mentor.ball),
                ]:
                    if getattr(profile, field) != value:
                        setattr(profile, field, value)
                        fields_to_update.append(field)
                if approve and not profile.tasdiqlangan:
                    profile.tasdiqlangan = True
                    fields_to_update.append("tasdiqlangan")
                if fields_to_update:
                    profile.save(update_fields=fields_to_update)
                    updated_profiles += 1

        self.stdout.write(self.style.SUCCESS(f"Users created: {created_users}"))
        self.stdout.write(self.style.SUCCESS(f"Mentor profiles created: {created_profiles}"))
        self.stdout.write(self.style.SUCCESS(f"Mentor profiles updated: {updated_profiles}"))

