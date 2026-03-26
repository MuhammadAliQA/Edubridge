"""
tests/test_forms.py  —  barcha formalar uchun validatsiya testlari

Ishga tushirish:
    python manage.py test tests.test_forms -v 2

Guruhlar:
    1. MentorRoyxatForm
    2. StudentRoyxatForm
    3. PaymentSubmissionForm
    4. BootstrapAdminForm
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import (
    MentorRoyxatForm,
    StudentRoyxatForm,
    PaymentSubmissionForm,
    BootstrapAdminForm,
)
from accounts.models import MentorProfile, StudentProfile, Enrollment, PaymentSubmission


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
MENTOR_BASE = {
    "username":      "mentor_test",
    "first_name":    "Saidalo",
    "last_name":     "Ibrohimov",
    "email":         "mentor@test.com",
    "password1":     "Str0ng!Pass99",
    "password2":     "Str0ng!Pass99",
    "viloyat":       "toshkent",
    "yonalish":      "ielts",
    "tajriba_yil":   2,
    "ball":          7.5,
    "haqida":        "IELTS bo'yicha 3 yillik tajribam bor.",
    "tajriba":       "Men 3 yildan beri IELTS o'qitib kelaman.",
    "metodologiya":  "Communicative va task-based metodlardan foydalanaman.",
    "muvaffaqiyat":  "O'quvchimdan biri IELTS 8.0 oldi.",
    "vaqt":          "Kechqurun 18:00-20:00",
    "maqsad":        "EduBridge orqali ko'proq o'quvchilarga yordam bermoqchiman.",
}

STUDENT_BASE = {
    "username":      "student_test",
    "first_name":    "Ali",
    "last_name":     "Valiyev",
    "email":         "student@test.com",
    "password1":     "Str0ng!Pass99",
    "password2":     "Str0ng!Pass99",
    "yosh":          20,
    "o_qish_joyi":   "TATU",
    "yashash_joyi":  "toshkent",
    "kutish":        "IELTS 7.0 olmoqchi va chet elda o'qishni rejalashtiryapman.",
}

PAYMENT_BASE = {
    "method":          "card",
    "transaction_ref": "TXN123456",
    "payer_name":      "Ali Valiyev",
    "payer_phone":     "+998901234567",
    "receipt_url":     "",
    "note":            "",
}


def mentor_data(**kwargs):
    return {**MENTOR_BASE, **kwargs}


def student_data(**kwargs):
    return {**STUDENT_BASE, **kwargs}


def payment_data(**kwargs):
    return {**PAYMENT_BASE, **kwargs}


# ═════════════════════════════════════════════════════════════
# 1. MENTOR RO'YXAT FORM
# ═════════════════════════════════════════════════════════════
class MentorFormValidTest(TestCase):

    def test_to_g_ri_ma_lumotlar(self):
        form = MentorRoyxatForm(data=mentor_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_ielts_ball_chegarasi(self):
        """IELTS ball 0-9 orasida bo'lishi kerak"""
        self.assertTrue(MentorRoyxatForm(data=mentor_data(ball=6.5)).is_valid())
        self.assertTrue(MentorRoyxatForm(data=mentor_data(ball=9.0)).is_valid())

    def test_sat_ball_to_g_ri(self):
        form = MentorRoyxatForm(data=mentor_data(yonalish="sat", ball=1400))
        self.assertTrue(form.is_valid(), form.errors)

    def test_ball_ixtiyoriy(self):
        """Ball bo'sh bo'lsa ham valid (ingliz_tili uchun)"""
        form = MentorRoyxatForm(data=mentor_data(yonalish="ingliz_tili", ball=""))
        self.assertTrue(form.is_valid(), form.errors)

    def test_save_mentor_profile_yaratadi(self):
        """save() chaqirilganda MentorProfile yaratilishi kerak"""
        form = MentorRoyxatForm(data=mentor_data())
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(MentorProfile.objects.filter(user=user).exists())


class MentorFormInvalidTest(TestCase):

    def test_ielts_ball_katta(self):
        """IELTS ball 9 dan katta bo'lsa xato"""
        form = MentorRoyxatForm(data=mentor_data(ball=9.5))
        self.assertFalse(form.is_valid())
        self.assertIn("ball", form.errors)

    def test_ielts_ball_manfiy(self):
        form = MentorRoyxatForm(data=mentor_data(ball=-1))
        self.assertFalse(form.is_valid())
        self.assertIn("ball", form.errors)

    def test_sat_ball_kichik(self):
        """SAT ball 400 dan kichik bo'lsa xato"""
        form = MentorRoyxatForm(data=mentor_data(yonalish="sat", ball=300))
        self.assertFalse(form.is_valid())
        self.assertIn("ball", form.errors)

    def test_sat_ball_katta(self):
        """SAT ball 1600 dan katta bo'lsa xato"""
        form = MentorRoyxatForm(data=mentor_data(yonalish="sat", ball=1700))
        self.assertFalse(form.is_valid())
        self.assertIn("ball", form.errors)

    def test_tajriba_qisqa(self):
        """tajriba 15 belgidan kam bo'lsa xato"""
        form = MentorRoyxatForm(data=mentor_data(tajriba="Oz tajriba"))
        self.assertFalse(form.is_valid())
        self.assertIn("tajriba", form.errors)

    def test_metodologiya_qisqa(self):
        form = MentorRoyxatForm(data=mentor_data(metodologiya="Yaxshi usul"))
        self.assertFalse(form.is_valid())
        self.assertIn("metodologiya", form.errors)

    def test_muvaffaqiyat_qisqa(self):
        form = MentorRoyxatForm(data=mentor_data(muvaffaqiyat="Yaxshi natija"))
        self.assertFalse(form.is_valid())
        self.assertIn("muvaffaqiyat", form.errors)

    def test_vaqt_qisqa(self):
        """vaqt 10 belgidan kam bo'lsa xato"""
        form = MentorRoyxatForm(data=mentor_data(vaqt="Kech"))
        self.assertFalse(form.is_valid())
        self.assertIn("vaqt", form.errors)

    def test_maqsad_qisqa(self):
        form = MentorRoyxatForm(data=mentor_data(maqsad="Pul topish"))
        self.assertFalse(form.is_valid())
        self.assertIn("maqsad", form.errors)

    def test_haqida_qisqa(self):
        """haqida kiritilgan bo'lsa kamida 15 ta belgi"""
        form = MentorRoyxatForm(data=mentor_data(haqida="Qisqa"))
        self.assertFalse(form.is_valid())
        self.assertIn("haqida", form.errors)

    def test_haqida_bosh_valid(self):
        """haqida bo'sh bo'lsa valid (ixtiyoriy)"""
        form = MentorRoyxatForm(data=mentor_data(haqida=""))
        self.assertTrue(form.is_valid(), form.errors)

    def test_email_takrorlanmas(self):
        """Avval ro'yxatdan o'tgan email bilan qayta bo'lmaydi"""
        User.objects.create_user(username="boshqa", email="mentor@test.com", password="x")
        form = MentorRoyxatForm(data=mentor_data())
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_username_majburiy(self):
        form = MentorRoyxatForm(data=mentor_data(username=""))
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_parol_mos_emas(self):
        form = MentorRoyxatForm(data=mentor_data(password2="BoshqaParol99!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_tajriba_faqat_son(self):
        """Faqat sonlardan iborat javob qabul qilinmasin"""
        form = MentorRoyxatForm(data=mentor_data(tajriba="123456789012345"))
        self.assertFalse(form.is_valid())
        self.assertIn("tajriba", form.errors)

    def test_yonalish_noto_g_ri(self):
        form = MentorRoyxatForm(data=mentor_data(yonalish="notvalid"))
        self.assertFalse(form.is_valid())
        self.assertIn("yonalish", form.errors)

    def test_viloyat_noto_g_ri(self):
        form = MentorRoyxatForm(data=mentor_data(viloyat="mars"))
        self.assertFalse(form.is_valid())
        self.assertIn("viloyat", form.errors)

    def test_tajriba_yil_manfiy(self):
        form = MentorRoyxatForm(data=mentor_data(tajriba_yil=-1))
        self.assertFalse(form.is_valid())
        self.assertIn("tajriba_yil", form.errors)

    def test_tajriba_yil_haddan_katta(self):
        form = MentorRoyxatForm(data=mentor_data(tajriba_yil=51))
        self.assertFalse(form.is_valid())
        self.assertIn("tajriba_yil", form.errors)


# ═════════════════════════════════════════════════════════════
# 2. STUDENT RO'YXAT FORM
# ═════════════════════════════════════════════════════════════
class StudentFormValidTest(TestCase):

    def test_to_g_ri_ma_lumotlar(self):
        form = StudentRoyxatForm(data=student_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_save_student_profile_yaratadi(self):
        form = StudentRoyxatForm(data=student_data())
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())

    def test_yosh_chegarasi_min(self):
        """7 yoshdan kichik bo'lmasin"""
        form = StudentRoyxatForm(data=student_data(yosh=7))
        self.assertTrue(form.is_valid(), form.errors)

    def test_yosh_chegarasi_max(self):
        form = StudentRoyxatForm(data=student_data(yosh=80))
        self.assertTrue(form.is_valid(), form.errors)


class StudentFormInvalidTest(TestCase):

    def test_yosh_kichik(self):
        form = StudentRoyxatForm(data=student_data(yosh=6))
        self.assertFalse(form.is_valid())
        self.assertIn("yosh", form.errors)

    def test_yosh_katta(self):
        form = StudentRoyxatForm(data=student_data(yosh=81))
        self.assertFalse(form.is_valid())
        self.assertIn("yosh", form.errors)

    def test_kutish_qisqa(self):
        """kutish 20 belgidan kam bo'lsa xato"""
        form = StudentRoyxatForm(data=student_data(kutish="Yaxshi o'qiyman"))
        self.assertFalse(form.is_valid())
        self.assertIn("kutish", form.errors)

    def test_kutish_faqat_son(self):
        form = StudentRoyxatForm(data=student_data(kutish="12345678901234567890"))
        self.assertFalse(form.is_valid())
        self.assertIn("kutish", form.errors)

    def test_o_qish_joyi_qisqa(self):
        """o'qish joyi 3 belgidan kam bo'lsa xato"""
        form = StudentRoyxatForm(data=student_data(o_qish_joyi="TT"))
        self.assertFalse(form.is_valid())
        self.assertIn("o_qish_joyi", form.errors)

    def test_o_qish_joyi_faqat_son(self):
        form = StudentRoyxatForm(data=student_data(o_qish_joyi="123"))
        self.assertFalse(form.is_valid())
        self.assertIn("o_qish_joyi", form.errors)

    def test_email_takrorlanmas(self):
        User.objects.create_user(username="boshqa", email="student@test.com", password="x")
        form = StudentRoyxatForm(data=student_data())
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_parol_mos_emas(self):
        form = StudentRoyxatForm(data=student_data(password2="WrongPass99!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_username_majburiy(self):
        form = StudentRoyxatForm(data=student_data(username=""))
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_email_format_noto_g_ri(self):
        form = StudentRoyxatForm(data=student_data(email="notanemail"))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_yashash_joyi_noto_g_ri(self):
        form = StudentRoyxatForm(data=student_data(yashash_joyi="mars"))
        self.assertFalse(form.is_valid())
        self.assertIn("yashash_joyi", form.errors)


# ═════════════════════════════════════════════════════════════
# 3. PAYMENT SUBMISSION FORM
# ═════════════════════════════════════════════════════════════
class PaymentFormValidTest(TestCase):

    def test_transaction_ref_bilan(self):
        form = PaymentSubmissionForm(data=payment_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_receipt_url_bilan(self):
        form = PaymentSubmissionForm(data=payment_data(
            transaction_ref="",
            receipt_url="https://drive.google.com/file/abc",
        ))
        self.assertTrue(form.is_valid(), form.errors)

    def test_ikkalasi_bilan(self):
        form = PaymentSubmissionForm(data=payment_data(
            receipt_url="https://t.me/chek",
        ))
        self.assertTrue(form.is_valid(), form.errors)

    def test_ixtiyoriy_fieldlar_bosh(self):
        form = PaymentSubmissionForm(data=payment_data(
            payer_name="", payer_phone="", note="",
        ))
        self.assertTrue(form.is_valid(), form.errors)

    def test_telefon_uzbek_format(self):
        form = PaymentSubmissionForm(data=payment_data(payer_phone="+998901234567"))
        self.assertTrue(form.is_valid(), form.errors)

    def test_telefon_bosh_valid(self):
        """Telefon ixtiyoriy"""
        form = PaymentSubmissionForm(data=payment_data(payer_phone=""))
        self.assertTrue(form.is_valid(), form.errors)


class PaymentFormInvalidTest(TestCase):

    def test_ikkalasi_bosh_xato(self):
        """transaction_ref ham, receipt_url ham bo'sh bo'lsa xato"""
        form = PaymentSubmissionForm(data=payment_data(
            transaction_ref="", receipt_url="",
        ))
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn(
            "Tranzaksiya ID yoki chek havolasidan kamida birini kiriting.",
            form.errors["__all__"],
        )

    def test_method_bosh(self):
        form = PaymentSubmissionForm(data=payment_data(method=""))
        self.assertFalse(form.is_valid())
        self.assertIn("method", form.errors)

    def test_telefon_qisqa(self):
        form = PaymentSubmissionForm(data=payment_data(payer_phone="+99890"))
        self.assertFalse(form.is_valid())
        self.assertIn("payer_phone", form.errors)

    def test_telefon_harfli(self):
        form = PaymentSubmissionForm(data=payment_data(payer_phone="abcdefghi"))
        self.assertFalse(form.is_valid())
        self.assertIn("payer_phone", form.errors)



    def test_method_noto_g_ri_tanlov(self):
        """Ruxsat etilmagan method xato berishi kerak"""
        form = PaymentSubmissionForm(data=payment_data(method="bitcoin"))
        self.assertFalse(form.is_valid())
        self.assertIn("method", form.errors)


# ═════════════════════════════════════════════════════════════
# 4. BOOTSTRAP ADMIN FORM
# ═════════════════════════════════════════════════════════════
class BootstrapAdminFormTest(TestCase):

    def _form(self, **kwargs):
        base = {
            "username":  "adminuser",
            "email":     "admin@test.com",
            "password1": "Str0ng!Pass99",
            "password2": "Str0ng!Pass99",
        }
        return BootstrapAdminForm(data={**base, **kwargs})

    def test_to_g_ri_ma_lumotlar(self):
        self.assertTrue(self._form().is_valid())

    def test_parol_mos_emas(self):
        form = self._form(password2="BoshqaParol")
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertIn("Parollar mos emas.", form.errors["password2"])

    def test_email_format_noto_g_ri(self):
        form = self._form(email="notanemail")
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_username_majburiy(self):
        form = self._form(username="")
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_parol_majburiy(self):
        form = self._form(password1="", password2="")
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)


# ═════════════════════════════════════════════════════════════
# 5. INTEGRATSIYA — form → save → DB
# ═════════════════════════════════════════════════════════════
class FormSaveIntegrationTest(TestCase):

    def test_mentor_save_db_da_saqlaydi(self):
        form = MentorRoyxatForm(data=mentor_data())
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(User.objects.filter(username="mentor_test").count(), 1)
        self.assertEqual(MentorProfile.objects.filter(user=user).count(), 1)
        profile = MentorProfile.objects.get(user=user)
        self.assertEqual(profile.yonalish, "ielts")
        self.assertEqual(profile.viloyat, "toshkent")
        self.assertFalse(profile.tasdiqlangan)  # default False bo'lishi kerak

    def test_student_save_db_da_saqlaydi(self):
        form = StudentRoyxatForm(data=student_data())
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(User.objects.filter(username="student_test").count(), 1)
        self.assertEqual(StudentProfile.objects.filter(user=user).count(), 1)
        profile = StudentProfile.objects.get(user=user)
        self.assertEqual(profile.yosh, 20)
        self.assertEqual(profile.yashash_joyi, "toshkent")

    def test_bir_xil_username_ikki_marta_yaratib_bolmaydi(self):
        form1 = StudentRoyxatForm(data=student_data())
        self.assertTrue(form1.is_valid())
        form1.save()

        form2 = StudentRoyxatForm(data=student_data(email="other@test.com"))
        self.assertFalse(form2.is_valid())
        self.assertIn("username", form2.errors)

    def test_bir_xil_email_ikki_marta_yaratib_bolmaydi(self):
        form1 = StudentRoyxatForm(data=student_data())
        self.assertTrue(form1.is_valid())
        form1.save()

        form2 = StudentRoyxatForm(data=student_data(username="student_test2"))
        self.assertFalse(form2.is_valid())
        self.assertIn("email", form2.errors)