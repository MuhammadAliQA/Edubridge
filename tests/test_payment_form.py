"""
accounts/tests/test_payment_form.py
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import PaymentSubmissionForm
from accounts.models import MentorProfile, StudentProfile, Enrollment, PaymentSubmission


def make_users():
    mentor_user = User.objects.create_user(
        username="mentor1", password="pass1234", first_name="Saidalo"
    )
    student_user = User.objects.create_user(
        username="student1", password="pass1234", first_name="Ali"
    )
    mentor = MentorProfile.objects.create(
        user=mentor_user,
        viloyat="toshkent",
        yonalish="ielts",
        tajriba_yil=2,
        tasdiqlangan=True,
    )
    student = StudentProfile.objects.create(
        user=student_user,
        yosh=20,
        o_qish_joyi="TATU",
        yashash_joyi="toshkent",
        kutish="IELTS 7.0 olmoqchiman",
    )
    enrollment = Enrollment.objects.create(
        student=student_user,
        mentor=mentor,
        yonalish="ielts",
    )
    return mentor_user, student_user, mentor, student, enrollment


class PaymentFormValidTest(TestCase):

    def test_transaction_ref_bilan_valid(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "TXN123456",
            "payer_name": "",
            "payer_phone": "",
            "receipt_url": "",
            "note": "",
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_receipt_url_bilan_valid(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "",
            "payer_name": "",
            "payer_phone": "",
            "receipt_url": "https://drive.google.com/file/abc123",
            "note": "",
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_ikkalasi_bilan_valid(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "TXN999",
            "payer_name": "Ali Valiyev",
            "payer_phone": "+998901234567",
            "receipt_url": "https://t.me/chek",
            "note": "IELTS kursi uchun",
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_barcha_ixtiyoriy_fieldlar_bosh(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "ABC",
            "payer_name": "",
            "payer_phone": "",
            "receipt_url": "",
            "note": "",
        })
        self.assertTrue(form.is_valid(), form.errors)


class PaymentFormInvalidTest(TestCase):

    def test_transaction_ref_va_receipt_url_ikkalasi_bosh(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "",
            "payer_name": "",
            "payer_phone": "",
            "receipt_url": "",
            "note": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn(
            "Tranzaksiya ID yoki chek havolasidan kamida birini kiriting.",
            form.errors["__all__"],
        )

    def test_method_bosh(self):
        form = PaymentSubmissionForm(data={
            "method": "",
            "transaction_ref": "TXN123",
            "payer_name": "",
            "payer_phone": "",
            "receipt_url": "",
            "note": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("method", form.errors)

    def test_telefon_qisqa(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "TXN123",
            "payer_name": "",
            "payer_phone": "+99890",
            "receipt_url": "",
            "note": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("payer_phone", form.errors)

    def test_telefon_noto_g_ri_format(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "TXN123",
            "payer_name": "",
            "payer_phone": "abcdefghi",
            "receipt_url": "",
            "note": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("payer_phone", form.errors)

    def test_receipt_url_noto_g_ri(self):
        form = PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "",
            "payer_name": "",
            "payer_phone": "",
            "receipt_url": "drive.google.com/abc",
            "note": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("receipt_url", form.errors)


class PhoneValidationTest(TestCase):

    def _form(self, phone):
        return PaymentSubmissionForm(data={
            "method": "card",
            "transaction_ref": "TXN1",
            "payer_name": "",
            "payer_phone": phone,
            "receipt_url": "",
            "note": "",
        })

    def test_uzbek_format_valid(self):
        self.assertTrue(self._form("+998901234567").is_valid())

    def test_uzbek_format_probelsiz_valid(self):
        self.assertTrue(self._form("998901234567").is_valid())

    def test_qisqa_raqam_invalid(self):
        self.assertFalse(self._form("12345").is_valid())

    def test_bosh_telefon_valid(self):
        self.assertTrue(self._form("").is_valid())


class PaymentSubmissionModelTest(TestCase):

    def setUp(self):
        _, _, _, _, self.enrollment = make_users()

    def test_submission_yaratish(self):
        sub = PaymentSubmission.objects.create(
            enrollment=self.enrollment,
            method="card",
            amount=150_000,
            transaction_ref="TXN001",
        )
        self.assertEqual(sub.status, PaymentSubmission.STATUS_PENDING)
        self.assertEqual(sub.amount, 150_000)

    def test_approve_enrollment_yangilanadi(self):
        sub = PaymentSubmission.objects.create(
            enrollment=self.enrollment,
            method="card",
            amount=150_000,
            transaction_ref="TXN002",
        )
        sub.status = PaymentSubmission.STATUS_APPROVED
        sub.save(update_fields=["status", "updated_at"])
        self.enrollment.to_langan = True
        self.enrollment.save(update_fields=["to_langan"])

        self.enrollment.refresh_from_db()
        self.assertTrue(self.enrollment.to_langan)

    def test_reject_enrollment_false_qoladi(self):
        sub = PaymentSubmission.objects.create(
            enrollment=self.enrollment,
            method="card",
            amount=150_000,
            transaction_ref="TXN003",
        )
        sub.status = PaymentSubmission.STATUS_REJECTED
        sub.save(update_fields=["status", "updated_at"])

        self.enrollment.refresh_from_db()
        self.assertFalse(self.enrollment.to_langan)

    def test_bir_enrollment_bir_nechta_submission(self):
        PaymentSubmission.objects.create(
            enrollment=self.enrollment,
            method="card",
            amount=150_000,
            transaction_ref="TXN_REJECTED",
            status=PaymentSubmission.STATUS_REJECTED,
        )
        sub2 = PaymentSubmission.objects.create(
            enrollment=self.enrollment,
            method="card",
            amount=150_000,
            transaction_ref="TXN_NEW",
        )
        self.assertEqual(
            PaymentSubmission.objects.filter(enrollment=self.enrollment).count(), 2
        )
        self.assertEqual(sub2.status, PaymentSubmission.STATUS_PENDING)

    def test_pending_holat_default(self):
        sub = PaymentSubmission.objects.create(
            enrollment=self.enrollment,
            method="card",
            amount=250_000,
            receipt_url="https://t.me/chek",
        )
        self.assertEqual(sub.status, PaymentSubmission.STATUS_PENDING)


class EnrollmentPaymentViewTest(TestCase):

    def setUp(self):
        _, self.student_user, _, self.student, self.enrollment = make_users()
        self.client.login(username="student1", password="pass1234")
        self.url = f"/to-lov/{self.enrollment.id}/"

    def test_to_langan_bo_lsa_redirect(self):
        self.enrollment.to_langan = True
        self.enrollment.save()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"/student/profil/{self.student.pk}/",
            fetch_redirect_response=False,
        )

    def test_login_talab_qilinadi(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/kirish/", response["Location"])