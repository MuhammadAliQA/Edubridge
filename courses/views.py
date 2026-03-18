from django.shortcuts import render, get_object_or_404
from accounts.models import MentorProfile, YONALISHLAR
from .models import FreeDars


def bosh_sahifa(request):
    top_ielts = MentorProfile.objects.filter(
        yonalish='ielts', tasdiqlangan=True
    ).order_by('-reytinq')[:3]

    top_sat = MentorProfile.objects.filter(
        yonalish='sat', tasdiqlangan=True
    ).order_by('-reytinq')[:3]

    top_ingliz = MentorProfile.objects.filter(
        yonalish='ingliz_tili', tasdiqlangan=True
    ).order_by('-reytinq')[:3]

    kelayotgan_free = FreeDars.objects.all().order_by('sana')[:5]

    context = {
        'top_ielts': top_ielts,
        'top_sat': top_sat,
        'top_ingliz': top_ingliz,
        'kelayotgan_free': kelayotgan_free,
        'narx': 300000,
        'mentor_ulushi': 200000,
    }
    return render(request, 'home/index.html', context)


def mentorlar(request):
    yonalish = request.GET.get('yonalish', '')
    viloyat = request.GET.get('viloyat', '')

    mentorlar_qs = MentorProfile.objects.filter(tasdiqlangan=True)

    if yonalish:
        mentorlar_qs = mentorlar_qs.filter(yonalish=yonalish)
    if viloyat:
        mentorlar_qs = mentorlar_qs.filter(viloyat=viloyat)

    mentorlar_qs = mentorlar_qs.order_by('-reytinq')

    from accounts.models import VILOYATLAR
    context = {
        'mentorlar': mentorlar_qs,
        'yonalishlar': YONALISHLAR,
        'viloyatlar': VILOYATLAR,
        'tanlangan_yonalish': yonalish,
        'tanlangan_viloyat': viloyat,
    }
    return render(request, 'courses/mentorlar.html', context)


def free_darslar(request):
    darslar = FreeDars.objects.all().order_by('sana')
    return render(request, 'courses/free_darslar.html', {'darslar': darslar})


def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk, tasdiqlangan=True)
    return render(request, 'courses/mentor_detail.html', {'mentor': mentor})


def ielts_sahifa(request):
    mentorlar = MentorProfile.objects.filter(
        yonalish='ielts', tasdiqlangan=True
    ).order_by('-reytinq')
    return render(request, 'courses/ielts.html', {'mentorlar': mentorlar})


def sat_sahifa(request):
    mentorlar = MentorProfile.objects.filter(
        yonalish='sat', tasdiqlangan=True
    ).order_by('-reytinq')
    return render(request, 'courses/sat.html', {'mentorlar': mentorlar})