from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import MentorProfile, StudentProfile, VILOYATLAR, YONALISHLAR
from .models import PaymentSubmission


class MentorRoyxatForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Ism", widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'}))
    last_name = forms.CharField(max_length=50, label="Familiya", widget=forms.TextInput(attrs={'placeholder': 'Familiyangiz'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email manzilingiz'}))
    viloyat = forms.ChoiceField(choices=VILOYATLAR, label="Viloyat")
    yonalish = forms.ChoiceField(choices=YONALISHLAR, label="Yo'nalish")
    tajriba_yil = forms.IntegerField(min_value=0, max_value=50, label="Tajriba (yil)", initial=1)
    ball = forms.FloatField(required=False, label="IELTS/SAT bali", widget=forms.NumberInput(attrs={'placeholder': '7.5 yoki 1400'}))
    haqida = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "O'zingiz haqingizda qisqacha..."}), label="O'zi haqida", required=False)
    
    # 5 ta savol
    tajriba = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="O'qitish tajribangizni tasvirlab bering")
    metodologiya = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Qanday metodologiya va usullardan foydalanasiz?")
    muvaffaqiyat = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="O'quvchilaringizdagi eng katta muvaffaqiyat qanday bo'lgan?")
    vaqt = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), label="Dars vaqtlari qanday bo'lishi mumkin?")
    maqsad = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="EduBridge'ga qo'shilish maqsadingiz nima?")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Foydalanuvchi nomi'
        self.fields['password1'].widget.attrs['placeholder'] = 'Parol'
        self.fields['password2'].widget.attrs['placeholder'] = 'Parolni tasdiqlang'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            MentorProfile.objects.create(
                user=user,
                viloyat=self.cleaned_data['viloyat'],
                yonalish=self.cleaned_data['yonalish'],
                tajriba_yil=self.cleaned_data['tajriba_yil'],
                ball=self.cleaned_data.get('ball'),
                haqida=self.cleaned_data.get('haqida', ''),
                tajriba=self.cleaned_data['tajriba'],
                metodologiya=self.cleaned_data['metodologiya'],
                muvaffaqiyat=self.cleaned_data['muvaffaqiyat'],
                vaqt=self.cleaned_data['vaqt'],
                maqsad=self.cleaned_data['maqsad'],
            )
        return user

    def clean_ball(self):
        ball = self.cleaned_data.get("ball")
        yonalish = self.cleaned_data.get("yonalish")
        if ball in (None, ""):
            return ball

        try:
            ball_f = float(ball)
        except (TypeError, ValueError):
            raise ValidationError("Ball noto'g'ri formatda.")

        if yonalish == "ielts":
            if not (0 < ball_f <= 9):
                raise ValidationError("IELTS band 0-9 oralig'ida bo'lishi kerak (masalan 7.5).")
        elif yonalish == "sat":
            if not (400 <= ball_f <= 1600):
                raise ValidationError("SAT ball 400-1600 oralig'ida bo'lishi kerak (masalan 1450).")
        else:
            return None

        return ball_f

    def clean(self):
        cleaned_data = super().clean()

        def _min_text(field_name: str, min_len: int = 15):
            value = (cleaned_data.get(field_name) or "").strip()
            if len(value) < min_len:
                self.add_error(field_name, f"Kamida {min_len} ta belgidan iborat bo'lsin.")
                return
            if value.isdigit():
                self.add_error(field_name, "Faqat son bo'lmasin, to'liq izoh yozing.")

        _min_text("tajriba", 15)
        _min_text("metodologiya", 15)
        _min_text("muvaffaqiyat", 15)
        _min_text("vaqt", 10)
        _min_text("maqsad", 15)

        haqida = (cleaned_data.get("haqida") or "").strip()
        if haqida and len(haqida) < 15:
            self.add_error("haqida", "Kamida 15 ta belgidan iborat bo'lsin.")

        return cleaned_data

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            return email
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Bu email bilan user allaqachon mavjud.")
        return email


class StudentRoyxatForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Ism", widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'}))
    last_name = forms.CharField(max_length=50, label="Familiya", widget=forms.TextInput(attrs={'placeholder': 'Familiyangiz'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email manzilingiz'}))
    yosh = forms.IntegerField(min_value=7, max_value=80, label="Yoshingiz")
    o_qish_joyi = forms.CharField(
        max_length=200,
        label="O'qish/ish joyingiz",
        widget=forms.TextInput(attrs={'placeholder': "Maktab/Universitet/Ish joyi (bitirgan bo'lsangiz ham yozing)"}),
    )
    yashash_joyi = forms.ChoiceField(choices=VILOYATLAR, label="Yashash joyingiz")
    kutish = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': "Bu dasturdan nima kutasiz? Qanday maqsadlaringiz bor?"}), label="Bu dasturdan nimalarni kutasiz?")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Foydalanuvchi nomi'
        self.fields['password1'].widget.attrs['placeholder'] = 'Parol'
        self.fields['password2'].widget.attrs['placeholder'] = 'Parolni tasdiqlang'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                yosh=self.cleaned_data['yosh'],
                o_qish_joyi=self.cleaned_data['o_qish_joyi'],
                yashash_joyi=self.cleaned_data['yashash_joyi'],
                kutish=self.cleaned_data['kutish'],
            )
        return user

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            return email
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Bu email bilan user allaqachon mavjud.")
        return email

    def clean_kutish(self):
        value = (self.cleaned_data.get("kutish") or "").strip()
        if len(value) < 20:
            raise ValidationError("Kamida 20 ta belgidan iborat bo'lsin.")
        if value.isdigit():
            raise ValidationError("Faqat son bo'lmasin, to'liq izoh yozing.")
        return value

    def clean_o_qish_joyi(self):
        value = (self.cleaned_data.get("o_qish_joyi") or "").strip()
        if len(value) < 3:
            raise ValidationError("Kamida 3 ta belgidan iborat bo'lsin.")
        if value.isdigit():
            raise ValidationError("Faqat son bo'lmasin.")
        return value


class BootstrapAdminForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "admin"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "admin@example.com"}),
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"placeholder": "Kuchli parol"}),
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={"placeholder": "Parolni qayta kiriting"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Parollar mos emas.")
        return cleaned_data


class PaymentSubmissionForm(forms.ModelForm):
    class Meta:
        model = PaymentSubmission
        fields = ["method", "payer_name", "payer_phone", "transaction_ref", "receipt_url", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3, "placeholder": "Masalan: qaysi mentor / qaysi sana"}),
            "transaction_ref": forms.TextInput(attrs={"placeholder": "ixtiyoriy"}),
            "payer_phone": forms.TextInput(attrs={"placeholder": "+998... (ixtiyoriy)"}),
            "payer_name": forms.TextInput(attrs={"placeholder": "ixtiyoriy"}),
            "receipt_url": forms.URLInput(attrs={"placeholder": "https://... (ixtiyoriy)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_payer_phone(self):
        phone = (self.cleaned_data.get("payer_phone") or "").strip()
        if not phone:
            return phone
        normalized = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
        if len([ch for ch in normalized if ch.isdigit()]) < 9:
            raise ValidationError("Telefon raqamni to'liq kiriting.")
        return phone
