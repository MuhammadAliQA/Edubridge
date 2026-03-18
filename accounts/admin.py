from django.contrib import admin
from .models import MentorProfile, StudentProfile, Enrollment

@admin.register(MentorProfile)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['user', 'viloyat', 'yonalish', 'tasdiqlangan', 'reytinq', 'o_quvchilar_soni']
    list_filter = ['viloyat', 'yonalish', 'tasdiqlangan']
    list_editable = ['tasdiqlangan']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']

@admin.register(StudentProfile)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'yosh', 'o_qish_joyi', 'yashash_joyi']
    list_filter = ['yashash_joyi']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'mentor', 'yonalish', 'to_langan', 'yaratilgan']
    list_filter = ['yonalish', 'to_langan']
    list_editable = ['to_langan']
