from django.db import models
from accounts.models import MentorProfile, YONALISHLAR

class Kurs(models.Model):
    """Mentor kursi"""
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='kurslar')
    yonalish = models.CharField(max_length=50, choices=YONALISHLAR)
    narx = models.PositiveIntegerField(default=300000, help_text="So'mda (1 hafta, 3 dars, 3 soatdan)")
    mentor_ulushi = models.PositiveIntegerField(default=200000, help_text="Mentorga to'lanadigan summa")
    haftada_dars = models.PositiveIntegerField(default=3)
    dars_davomiyligi = models.PositiveIntegerField(default=3, help_text="Soatda")
    haqida = models.TextField(blank=True)
    faol = models.BooleanField(default=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
    
    def __str__(self):
        return f"{self.mentor} - {self.get_yonalish_display()}"


class FreeDars(models.Model):
    """Bepul IELTS/SAT darslari - haftada 1 marta, 1.5 soat"""
    PLATFORM_MEET = "meet"
    PLATFORM_ZOOM = "zoom"
    PLATFORM_OTHER = "other"

    PLATFORM_CHOICES = [
        (PLATFORM_MEET, "Google Meet"),
        (PLATFORM_ZOOM, "Zoom"),
        (PLATFORM_OTHER, "Boshqa"),
    ]

    sarlavha = models.CharField(max_length=200)
    yonalish = models.CharField(max_length=50, choices=YONALISHLAR)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='free_darslar')
    sana = models.DateTimeField()
    davomiylik = models.PositiveIntegerField(default=90, help_text="Daqiqada (1.5 soat = 90 daqiqa)")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default=PLATFORM_MEET)
    link = models.URLField(blank=True, help_text="Zoom/Meet havolasi")
    haqida = models.TextField(blank=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Bepul dars"
        verbose_name_plural = "Bepul darslar"
        ordering = ['-sana']
    
    def __str__(self):
        return f"{self.sarlavha} - {self.sana.strftime('%d.%m.%Y')}"

    @property
    def platform_label(self) -> str:
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)
