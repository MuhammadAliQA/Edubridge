import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MentorRoyxatForm, StudentRoyxatForm, BootstrapAdminForm, PaymentSubmissionForm
from .models import MentorProfile, StudentProfile, Enrollment, PaymentSubmission, YONALISHLAR


def mentor_royxat(request):
    if request.user.is_authenticated:
        messages.info(request, "Siz allaqachon kirgansiz.")
        if hasattr(request.user, "mentor_profile"):
            return redirect("mentor_profil", pk=request.user.mentor_profile.pk)
        if hasattr(request.user, "student_profile"):
            return redirect("student_profil", pk=request.user.student_profile.pk)
        return redirect("/")

    if request.method == 'POST':
        form = MentorRoyxatForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Mentor sifatida ro'yxatdan o'tdingiz! Endi hisobingizga kiring — profilingiz admin tomonidan tekshiriladi.",
            )
            return redirect(f"/kirish/?username={user.username}&registered=1")
    else:
        form = MentorRoyxatForm()
    return render(request, 'accounts/mentor_royxat.html', {'form': form})


def student_royxat(request):
    if request.user.is_authenticated:
        messages.info(request, "Siz allaqachon kirgansiz.")
        if hasattr(request.user, "student_profile"):
            return redirect("student_profil", pk=request.user.student_profile.pk)
        if hasattr(request.user, "mentor_profile"):
            return redirect("mentor_profil", pk=request.user.mentor_profile.pk)
        return redirect("/")

    if request.method == 'POST':
        form = StudentRoyxatForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi hisobingizga kiring.")
            return redirect(f"/kirish/?username={user.username}&registered=1")
    else:
        form = StudentRoyxatForm()
    return render(request, 'accounts/student_royxat.html', {'form': form})


def kirish(request):
    if request.user.is_authenticated:
        messages.info(request, "Siz allaqachon kirgansiz.")
        return redirect("/")

    if request.method == "GET" and request.GET.get("registered") == "1":
        messages.success(request, "Ro'yxatdan o'tish yakunlandi. Endi login qiling.")

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if not user and "@" in username:
            try:
                by_email = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                by_email = None
            if by_email:
                user = authenticate(request, username=by_email.username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}!")
            return redirect('/')
        else:
            messages.error(request, "Username yoki parol noto'g'ri!")
    return render(
        request,
        "accounts/kirish.html",
        {"default_username": (request.GET.get("username") or "").strip()},
    )


@login_required
def chiqish(request):
    logout(request)
    return redirect('/')


def mentor_profil(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    enrollments = mentor.enrollments.all()

    my_enrollment = None
    my_latest_payment = None
    if request.user.is_authenticated:
        my_enrollment = Enrollment.objects.filter(
            student=request.user,
            mentor=mentor,
            yonalish=mentor.yonalish,
        ).first()
        if my_enrollment:
            my_latest_payment = my_enrollment.payment_submissions.first()

    return render(
        request,
        "accounts/mentor_profil.html",
        {
            "mentor": mentor,
            "enrollments": enrollments,
            "my_enrollment": my_enrollment,
            "my_latest_payment": my_latest_payment,
        },
    )


@login_required
def student_profil(request, pk):
    if not hasattr(request.user, "student_profile") and not request.user.is_staff:
        messages.info(request, "Student profilingiz yo'q. Avval ro'yxatdan o'ting.")
        return redirect("student_royxat")

    student = get_object_or_404(StudentProfile, pk=pk)
    if student.user_id != request.user.id and not request.user.is_staff:
        raise Http404()

    enrollments = Enrollment.objects.filter(student=student.user)
    latest_payments = {
        enrollment.id: enrollment.payment_submissions.first()
        for enrollment in enrollments.select_related("mentor", "student").prefetch_related("payment_submissions")
    }
    return render(
        request,
        "accounts/student_profil.html",
        {"student": student, "enrollments": enrollments, "latest_payments": latest_payments},
    )


@login_required
def kursga_yozilish(request, mentor_pk, yonalish):
    if not hasattr(request.user, "student_profile") and not request.user.is_staff:
        messages.info(request, "Kursga yozilish uchun o'quvchi sifatida ro'yxatdan o'ting.")
        return redirect("student_royxat")

    valid_yonalishlar = {val for val, _label in YONALISHLAR}
    if yonalish not in valid_yonalishlar:
        raise Http404()

    mentor = get_object_or_404(MentorProfile, pk=mentor_pk, tasdiqlangan=True)
    if mentor.yonalish != yonalish:
        raise Http404()
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        mentor=mentor,
        yonalish=yonalish
    )
    if created:
        messages.success(request, f"{mentor.get_yonalish_display()} kursiga yozildingiz! To'lovni yakunlang.")
        return redirect("enrollment_payment", enrollment_id=enrollment.id)
    else:
        messages.info(request, "Siz allaqachon bu kursga yozilgansiz.")
    return redirect('mentorlar')


def bootstrap_admin(request, token: str):
    bootstrap_token = (os.environ.get("BOOTSTRAP_ADMIN_TOKEN") or "").strip()
    if not bootstrap_token or token != bootstrap_token:
        raise Http404()

    if User.objects.filter(is_superuser=True).exists():
        admin_path = (os.environ.get("ADMIN_PATH") or "").strip()
        if not admin_path:
            admin_path = "admin/" if settings.DEBUG else "secure-admin/"
        if not admin_path.startswith("/"):
            admin_path = "/" + admin_path
        return redirect(admin_path)

    if request.method == "POST":
        form = BootstrapAdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            if User.objects.filter(username=username).exists():
                form.add_error("username", "Bu username band.")
            elif User.objects.filter(email=email).exists():
                form.add_error("email", "Bu email band.")
            else:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                messages.success(
                    request,
                    "Admin yaratildi. Endi admin panelga login qiling.",
                )
                admin_path = os.environ.get("ADMIN_PATH")
                if admin_path is None:
                    admin_path = "admin/" if settings.DEBUG else "secure-admin/"
                if not admin_path.startswith("/"):
                    admin_path = "/" + admin_path
                return redirect(admin_path)
    else:
        form = BootstrapAdminForm()

    return render(request, "accounts/bootstrap_admin.html", {"form": form})


@login_required
def enrollment_payment(request, enrollment_id: int):
    if not hasattr(request.user, "student_profile") and not request.user.is_staff:
        messages.info(request, "To'lov uchun o'quvchi sifatida ro'yxatdan o'ting.")
        return redirect("student_royxat")

    enrollment = get_object_or_404(Enrollment, pk=enrollment_id, student=request.user)

    if enrollment.to_langan:
        messages.info(request, "To'lov allaqachon tasdiqlangan.")
        if hasattr(request.user, "student_profile"):
            return redirect("student_profil", pk=request.user.student_profile.pk)
        return redirect("/")

    expected_amount = 250000 if enrollment.yonalish == "ingliz_tili" else 150000
    latest_submission = enrollment.payment_submissions.first()
    if latest_submission and latest_submission.status == PaymentSubmission.STATUS_PENDING and request.method != "GET":
        messages.info(request, "To'lov arizasi allaqachon yuborilgan. Admin tekshiradi.")
        return redirect("enrollment_payment", enrollment_id=enrollment.id)

    if request.method == "POST":
        form = PaymentSubmissionForm(request.POST)
        if form.is_valid():
            submission: PaymentSubmission = form.save(commit=False)
            submission.enrollment = enrollment
            submission.amount = expected_amount
            submission.save()
            messages.success(request, "To'lov ma'lumotingiz yuborildi. Admin tekshiradi.")
            return redirect("student_profil", pk=request.user.student_profile.pk)
    else:
        form = PaymentSubmissionForm()

    payment_details = {
        "card_owner": os.environ.get("PAYMENT_CARD_OWNER", ""),
        "card_number": os.environ.get("PAYMENT_CARD_NUMBER", ""),
        "phone": os.environ.get("PAYMENT_PHONE", ""),
        "telegram": os.environ.get("PAYMENT_TELEGRAM", ""),
    }

    return render(
        request,
        "accounts/enrollment_payment.html",
        {
            "enrollment": enrollment,
            "expected_amount": expected_amount,
            "form": form,
            "payment_details": payment_details,
            "latest_submission": latest_submission,
        },
    )
