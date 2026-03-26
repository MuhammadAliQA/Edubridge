from django.db import models
from django.contrib.auth.models import User

VILOYATLAR = [
    ('toshkent_sh', 'Toshkent shahri'),
    ('toshkent', 'Toshkent viloyati'),
    ('andijon', 'Andijon'),
    ('fargona', 'Farg\'ona'),
    ('namangan', 'Namangan'),
    ('samarqand', 'Samarqand'),
    ('buxoro', 'Buxoro'),
    ('qashqadaryo', 'Qashqadaryo'),
    ('surxondaryo', 'Surxondaryo'),
    ('jizzax', 'Jizzax'),
    ('sirdaryo', 'Sirdaryo'),
    ('navoiy', 'Navoiy'),
    ('xorazm', 'Xorazm'),
    ('qoraqalpogiston', 'Qoraqalpog\'iston'),
]

YONALISHLAR = [
    ('ielts', 'IELTS'),
    ('sat', 'SAT'),
    ('ingliz_tili', 'Admission'),
    ('grants', 'Grants'),
]

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    viloyat = models.CharField(max_length=50, choices=VILOYATLAR)
    yonalish = models.CharField(max_length=50, choices=YONALISHLAR)
    tajriba_yil = models.PositiveIntegerField(default=1, verbose_name="Tajriba (yil)")
    haqida = models.TextField(blank=True, verbose_name="O'zi haqida")
    ball = models.FloatField(null=True, blank=True, verbose_name="IELTS/SAT bali")
    

    tajriba = models.TextField(verbose_name="O'qitish tajribangiz?")
    metodologiya = models.TextField(verbose_name="Qanday metodologiya ishlatiladi?")
    muvaffaqiyat = models.TextField(verbose_name="O'quvchilardagi eng katta muvaffaqiyat?")
    vaqt = models.TextField(verbose_name="Dars vaqtlari qanday bo'ladi?")
    maqsad = models.TextField(verbose_name="EduBridge'ga qo'shilish maqsadingiz?")
    
    rasm = models.ImageField(upload_to='mentor_rasmlari/', blank=True, null=True)
    reytinq = models.FloatField(default=0.0)
    o_quvchilar_soni = models.PositiveIntegerField(default=0)
    tasdiqlangan = models.BooleanField(default=False)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Mentor profili"
        verbose_name_plural = "Mentor profillari"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_yonalish_display()}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    yosh = models.PositiveIntegerField(verbose_name="Yoshi")
    o_qish_joyi = models.CharField(max_length=200, verbose_name="O'qish joyi")
    yashash_joyi = models.CharField(max_length=100, choices=VILOYATLAR, verbose_name="Yashash joyi")
    kutish = models.TextField(verbose_name="Bu dasturdan nimalarni kutasiz?")
    rasm = models.ImageField(upload_to='student_rasmlari/', blank=True, null=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "O'quvchi profili"
        verbose_name_plural = "O'quvchi profillari"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.yosh} yosh"


class Enrollment(models.Model):
    """O'quvchi kursga yozilishi"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='enrollments')
    yonalish = models.CharField(max_length=50, choices=YONALISHLAR)
    to_langan = models.BooleanField(default=False)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'mentor', 'yonalish')
        verbose_name = "Yozilish"
        verbose_name_plural = "Yozilishlar"
    
    def __str__(self):
        return f"{self.student.username} → {self.mentor}"


class PaymentSubmission(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Kutilmoqda"),
        (STATUS_APPROVED, "Tasdiqlandi"),
        (STATUS_REJECTED, "Rad etildi"),
    ]

    METHOD_CARD = "card"
    METHOD_CASH = "cash"
    METHOD_PAYME = "payme"
    METHOD_CLICK = "click"
    METHOD_OTHER = "other"

    METHOD_CHOICES = [
        (METHOD_CARD, "Karta"),
        (METHOD_PAYME, "Payme"),
        (METHOD_CLICK, "Click"),
        (METHOD_CASH, "Naqd"),
        (METHOD_OTHER, "Boshqa"),
    ]

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="payment_submissions",
        verbose_name="Yozilish",
    )
    amount = models.PositiveIntegerField(verbose_name="Summa (so'm)")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=METHOD_CARD)
    payer_name = models.CharField(max_length=120, blank=True, verbose_name="To'lov qiluvchi (ixtiyoriy)")
    payer_phone = models.CharField(max_length=50, blank=True, verbose_name="Telefon (ixtiyoriy)")
    transaction_ref = models.CharField(max_length=120, blank=True, verbose_name="Tranzaksiya ID (ixtiyoriy)")
    receipt_url = models.URLField(blank=True, verbose_name="Chek havolasi (ixtiyoriy)")
    note = models.TextField(blank=True, verbose_name="Izoh (ixtiyoriy)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "To'lov arizasi"
        verbose_name_plural = "To'lov arizalari"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.enrollment_id} - {self.amount} - {self.status}"

    @property
    def expected_amount(self) -> int:
        return 250000 if self.enrollment.yonalish == "ingliz_tili" else 150000

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.STATUS_APPROVED:
            Enrollment.objects.filter(pk=self.enrollment_id).update(to_langan=True)
