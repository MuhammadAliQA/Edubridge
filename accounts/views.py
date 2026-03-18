from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MentorRoyxatForm, StudentRoyxatForm
from .models import MentorProfile, StudentProfile, Enrollment


def mentor_royxat(request):
    if request.method == 'POST':
        form = MentorRoyxatForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Mentor sifatida ro'yxatdan o'tdingiz! Profilingiz tekshirilmoqda.")
            return redirect('mentor_profil', pk=user.mentor_profile.pk)
    else:
        form = MentorRoyxatForm()
    return render(request, 'accounts/mentor_royxat.html', {'form': form})


def student_royxat(request):
    if request.method == 'POST':
        form = StudentRoyxatForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('student_profil', pk=user.student_profile.pk)
    else:
        form = StudentRoyxatForm()
    return render(request, 'accounts/student_royxat.html', {'form': form})


def kirish(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}!")
            return redirect('/')
        else:
            messages.error(request, "Username yoki parol noto'g'ri!")
    return render(request, 'accounts/kirish.html')


@login_required
def chiqish(request):
    logout(request)
    return redirect('/')


def mentor_profil(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    enrollments = mentor.enrollments.all()
    return render(request, 'accounts/mentor_profil.html', {'mentor': mentor, 'enrollments': enrollments})


def student_profil(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    enrollments = Enrollment.objects.filter(student=student.user)
    return render(request, 'accounts/student_profil.html', {'student': student, 'enrollments': enrollments})


@login_required
def kursga_yozilish(request, mentor_pk, yonalish):
    mentor = get_object_or_404(MentorProfile, pk=mentor_pk)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        mentor=mentor,
        yonalish=yonalish
    )
    if created:
        messages.success(request, f"{mentor.get_yonalish_display()} kursiga yozildingiz!")
    else:
        messages.info(request, "Siz allaqachon bu kursga yozilgansiz.")
    return redirect('mentorlar')
