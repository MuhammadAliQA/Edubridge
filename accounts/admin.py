from django.contrib import admin
from .models import MentorProfile, StudentProfile, Enrollment, PaymentSubmission


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
    search_fields = ['student__username', 'mentor__user__username']


@admin.register(PaymentSubmission)
class PaymentSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'enrollment', 'amount', 'method', 'status',
        'created_at', 'student_name', 'mentor_name', 'yonalish_display',
    ]
    list_filter = ['status', 'method', 'enrollment__yonalish']
    search_fields = [
        'enrollment__student__username',
        'enrollment__student__first_name',
        'enrollment__mentor__user__username',
        'transaction_ref',
        'payer_phone',
        'payer_name',
    ]
    list_editable = ['status']
    actions = ['approve_selected', 'reject_selected']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('enrollment', 'status', 'method', 'amount')
        }),
        ('To\'lov tafsilotlari', {
            'fields': ('payer_name', 'payer_phone', 'transaction_ref', 'receipt_url', 'note')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # ── display helpers ──────────────────────────────────────────────────────
    @admin.display(description='Student')
    def student_name(self, obj):
        return obj.enrollment.student.get_full_name() or obj.enrollment.student.username

    @admin.display(description='Mentor')
    def mentor_name(self, obj):
        return obj.enrollment.mentor.user.get_full_name() or obj.enrollment.mentor.user.username

    @admin.display(description='Yo\'nalish')
    def yonalish_display(self, obj):
        return obj.enrollment.get_yonalish_display()

    # ── actions ──────────────────────────────────────────────────────────────
    @admin.action(description="✅ Tanlangan to'lovlarni tasdiqlash")
    def approve_selected(self, request, queryset):
        updated = 0
        for submission in queryset.select_related('enrollment'):
            if submission.status != PaymentSubmission.STATUS_APPROVED:
                submission.status = PaymentSubmission.STATUS_APPROVED
                submission.save(update_fields=['status', 'updated_at'])

                # FIX: Enrollment.to_langan = True — asosiy tuzatish
                enrollment = submission.enrollment
                if not enrollment.to_langan:
                    enrollment.to_langan = True
                    enrollment.save(update_fields=['to_langan'])

                updated += 1
        self.message_user(request, f"✅ Tasdiqlandi: {updated} ta to'lov. Enrollment ham yangilandi.")

    @admin.action(description="❌ Tanlangan to'lovlarni rad etish")
    def reject_selected(self, request, queryset):
        updated = 0
        for submission in queryset.select_related('enrollment'):
            if submission.status != PaymentSubmission.STATUS_REJECTED:
                submission.status = PaymentSubmission.STATUS_REJECTED
                submission.save(update_fields=['status', 'updated_at'])

                # Agar shu enrollment ning barcha submission lari rejected bo'lsa,
                # to_langan ni False ga qaytarish (ehtiyot uchun)
                enrollment = submission.enrollment
                has_approved = enrollment.payment_submissions.filter(
                    status=PaymentSubmission.STATUS_APPROVED
                ).exists()
                if not has_approved and enrollment.to_langan:
                    enrollment.to_langan = False
                    enrollment.save(update_fields=['to_langan'])

                updated += 1
        self.message_user(request, f"❌ Rad etildi: {updated} ta to'lov.")