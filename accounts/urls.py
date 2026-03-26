from django.urls import path
from . import views

urlpatterns = [
    path('mentor/royxat/', views.mentor_royxat, name='mentor_royxat'),
    path('student/royxat/', views.student_royxat, name='student_royxat'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),
    path('mentor/profil/<int:pk>/', views.mentor_profil, name='mentor_profil'),
    path('student/profil/<int:pk>/', views.student_profil, name='student_profil'),
    path('kurs/yozilish/<int:mentor_pk>/<str:yonalish>/', views.kursga_yozilish, name='kursga_yozilish'),
    path('payment/<int:enrollment_id>/', views.enrollment_payment, name='enrollment_payment'),
    path('setup-admin/<str:token>/', views.bootstrap_admin, name='bootstrap_admin'),
]
