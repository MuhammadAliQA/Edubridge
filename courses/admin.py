from django.contrib import admin
from .models import Kurs, FreeDars

@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'yonalish', 'narx', 'faol']
    list_filter = ['yonalish', 'faol']
    list_editable = ['faol']

@admin.register(FreeDars)
class FreeDarsAdmin(admin.ModelAdmin):
    list_display = ['sarlavha', 'yonalish', 'mentor', 'sana', 'davomiylik']
    list_filter = ['yonalish']
    ordering = ['sana']
