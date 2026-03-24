from django.urls import path
from . import views

urlpatterns = [
    path('healthz/', views.healthz, name='healthz'),
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('mentorlar/', views.mentorlar, name='mentorlar'),
    path('mentor/<int:pk>/', views.mentor_detail, name='mentor_detail'),
    path('free-darslar/', views.free_darslar, name='free_darslar'),
    path('kurs/ielts/', views.ielts_sahifa, name='ielts_sahifa'),
    path('kurs/sat/', views.sat_sahifa, name='sat_sahifa'),
    path('admission/', views.admission, name='admission'),
    path('grants/', views.grants, name='grants'),
    ]
