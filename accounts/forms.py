from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MentorProfile, StudentProfile, VILOYATLAR, YONALISHLAR


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


class StudentRoyxatForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Ism", widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'}))
    last_name = forms.CharField(max_length=50, label="Familiya", widget=forms.TextInput(attrs={'placeholder': 'Familiyangiz'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email manzilingiz'}))
    yosh = forms.IntegerField(min_value=10, max_value=50, label="Yoshingiz")
    o_qish_joyi = forms.CharField(max_length=200, label="O'qish joyingiz", widget=forms.TextInput(attrs={'placeholder': 'Maktab/Universitet nomi'}))
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
