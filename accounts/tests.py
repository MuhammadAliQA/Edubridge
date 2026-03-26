import os
import unittest

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from accounts.models import MentorProfile, StudentProfile, Enrollment


class AuthPagesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_auth_pages_load(self):
        for url in ["/kirish/", "/mentor/royxat/", "/student/royxat/"]:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 200)

    def test_login_with_wrong_credentials(self):
        resp = self.client.post("/kirish/", {"username": "notexist", "password": "wrongpass"})
        self.assertEqual(resp.status_code, 200)

    def test_register_pages_redirect_when_authenticated(self):
        user = User.objects.create_user(username="u1", password="pass12345")
        self.client.login(username="u1", password="pass12345")
        self.assertEqual(self.client.get("/student/royxat/").status_code, 302)
        self.assertEqual(self.client.get("/mentor/royxat/").status_code, 302)
        self.assertEqual(self.client.get("/kirish/").status_code, 302)


class EnrollmentFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(username="student", password="pass12345")
        StudentProfile.objects.create(
            user=self.student_user,
            yosh=18,
            o_qish_joyi="Toshkent",
            yashash_joyi="toshkent_sh",
            kutish="IELTS uchun mentor bilan ishlamoqchiman.",
        )
        self.mentor_user = User.objects.create_user(username="mentor", password="pass12345")
        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            viloyat="toshkent_sh",
            yonalish="ielts",
            tajriba_yil=1,
            ball=7.5,
            haqida="About",
            tajriba="Teaching experience text",
            metodologiya="Methods text",
            muvaffaqiyat="Success text",
            vaqt="Evenings",
            maqsad="Goal text",
            tasdiqlangan=True,
        )

    def test_invalid_direction_404(self):
        self.client.login(username="student", password="pass12345")
        resp = self.client.get(f"/kurs/yozilish/{self.mentor.pk}/unknown/")
        self.assertEqual(resp.status_code, 404)

    def test_enroll_redirects_and_creates_enrollment(self):
        self.client.login(username="student", password="pass12345")
        resp = self.client.get(f"/kurs/yozilish/{self.mentor.pk}/ielts/")
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            Enrollment.objects.filter(student=self.student_user, mentor=self.mentor, yonalish="ielts").exists()
        )


class TranslationsTest(TestCase):
    def test_translations_json_exists(self):
        import os
        from django.conf import settings

        path = os.path.join(settings.BASE_DIR, "static", "translations.json")
        self.assertTrue(os.path.exists(path), "translations.json topilmadi")

    def test_translations_has_all_languages(self):
        import json
        import os
        from django.conf import settings

        path = os.path.join(settings.BASE_DIR, "static", "translations.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("uz", data)
        self.assertIn("en", data)
        self.assertIn("ru", data)

    def test_translations_key_counts_match(self):
        import json
        import os
        from django.conf import settings

        path = os.path.join(settings.BASE_DIR, "static", "translations.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        uz_keys = set(data["uz"].keys())
        en_keys = set(data["en"].keys())
        ru_keys = set(data["ru"].keys())
        missing_en = uz_keys - en_keys
        missing_ru = uz_keys - ru_keys
        self.assertEqual(len(missing_en), 0, f"EN da yetishmayotgan kalitlar: {missing_en}")
        self.assertEqual(len(missing_ru), 0, f"RU da yetishmayotgan kalitlar: {missing_ru}")


try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    SELENIUM_AVAILABLE = True
except Exception:  # pragma: no cover
    SELENIUM_AVAILABLE = False


@unittest.skipUnless(
    SELENIUM_AVAILABLE and os.environ.get("RUN_SELENIUM_TESTS") == "1",
    "Selenium tests disabled. Install selenium + set RUN_SELENIUM_TESTS=1.",
)
class SeleniumE2ETest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = cls._create_driver()
        cls.wait = WebDriverWait(cls.driver, 5)

    @classmethod
    def tearDownClass(cls):
        try:
            if getattr(cls, "driver", None):
                cls.driver.quit()
        finally:
            super().tearDownClass()

    @classmethod
    def _create_driver(cls):
        browser = (os.environ.get("SELENIUM_BROWSER") or "chrome").strip().lower()
        try:
            if browser == "firefox":
                options = webdriver.FirefoxOptions()
                options.add_argument("-headless")
                return webdriver.Firefox(options=options)

            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280,900")
            options.add_argument("--no-sandbox")
            return webdriver.Chrome(options=options)
        except WebDriverException as exc:  # pragma: no cover
            raise unittest.SkipTest(
                f"Selenium driver not available ({browser}). "
                "Install a browser + driver (chromedriver/geckodriver) and ensure it's on PATH. "
                f"Original error: {exc}"
            )

    def test_homepage_loads(self):
        self.driver.get(f"{self.live_server_url}/")
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertIn("EduBridge", body.text)

    def test_student_register_redirects_to_login(self):
        self.driver.get(f"{self.live_server_url}/student/royxat/")

        self.driver.find_element(By.NAME, "first_name").send_keys("Test")
        self.driver.find_element(By.NAME, "last_name").send_keys("Student")
        self.driver.find_element(By.NAME, "email").send_keys("test.student@example.com")
        self.driver.find_element(By.NAME, "username").send_keys("test_student")
        self.driver.find_element(By.NAME, "yosh").send_keys("18")
        self.driver.find_element(By.NAME, "password1").send_keys("StrongPass12345!")
        self.driver.find_element(By.NAME, "password2").send_keys("StrongPass12345!")
        self.driver.find_element(By.NAME, "o_qish_joyi").send_keys("Graduate / Working")
        self.driver.find_element(By.NAME, "yashash_joyi").send_keys("Toshkent shahri")
        self.driver.find_element(By.NAME, "kutish").send_keys("IELTS va SAT bo'yicha mentor bilan ishlamoqchiman.")

        self.driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()
        self.wait.until(lambda d: "/kirish/" in d.current_url)
        self.assertIn("/kirish/", self.driver.current_url)
