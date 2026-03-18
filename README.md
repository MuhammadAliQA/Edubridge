# 🎓 EduBridge — Django Web Platformasi

IELTS, SAT va Ingliz tili bo'yicha mentor va o'quvchilarni bog'lovchi platforma.

---

## 🚀 Ishga tushirish

### 1. Virtual muhit yaratish
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini sozlash
```bash
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py migrate
```

### 4. Superuser yaratish (Admin panel uchun)
```bash
python manage.py createsuperuser
```

### 5. Serverni ishga tushirish
```bash
python manage.py runserver
```

Sayt: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin/

---

## 📋 Sahifalar

| URL | Sahifa |
|-----|--------|
| `/` | Bosh sahifa |
| `/mentorlar/` | Mentorlar ro'yxati (filter bilan) |
| `/mentor/<id>/` | Mentor profili |
| `/free-darslar/` | Bepul IELTS/SAT darslari |
| `/mentor/royxat/` | Mentor ro'yxati (5 savol bilan) |
| `/student/royxat/` | O'quvchi ro'yxati |
| `/kirish/` | Kirish |
| `/admin/` | Admin panel |

---

## 🔧 Funksiyalar

### Mentor uchun:
- ✅ Alohida ro'yxat formasi (5 ta savol)
- ✅ Har bir viloyatdan qabul
- ✅ Admin tomonidan tasdiqlash
- ✅ Profil sahifasi (savollar, statistika, narx)
- ✅ Bepul darslar o'tkazish

### O'quvchi uchun:
- ✅ Alohida ro'yxat formasi
- ✅ Profil: ism, yoshi, email, o'qish joyi, yashash joyi, maqsad
- ✅ Mentor tanlash va kursga yozilish
- ✅ Yozilgan kurslar ro'yxati

### Kurs:
- ✅ 3 yo'nalish: IELTS, SAT, Ingliz tili
- ✅ Narx: 300,000 so'm (hafta, 3 dars, 3 soatdan)
- ✅ Mentor ulushi: 200,000 so'm/o'quvchi
- ✅ Bepul darslar: haftada 1 marta, 1.5 soat

---

## 🏗️ Loyiha tuzilmasi

```
edubridge/
├── edubridge/          # Asosiy sozlamalar
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/           # Foydalanuvchi ilovasi
│   ├── models.py       # MentorProfile, StudentProfile, Enrollment
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── courses/            # Kurslar ilovasi
│   ├── models.py       # Kurs, FreeDars
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/          # HTML shablonlar
│   ├── base.html
│   ├── home/
│   ├── accounts/
│   └── courses/
├── static/             # CSS, JS, rasmlar
├── manage.py
└── requirements.txt
```

---

## 👨‍💻 Texnologiyalar
- **Backend:** Django 4.2
- **Database:** SQLite (mahalliy), PostgreSQL (production uchun)
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Shriftlar:** Plus Jakarta Sans, Syne (Google Fonts)

---

## 📞 Qo'shimcha sozlamalar

Production uchun `settings.py` da o'zgartiring:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-secret-key-here'

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edubridge_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
