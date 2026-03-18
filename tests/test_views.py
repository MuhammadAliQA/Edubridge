from django.test import TestCase, Client
from django.urls import reverse


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_contains_edubridge(self):
        response = self.client.get('/')
        self.assertContains(response, 'EduBridge')

    def test_mentorlar_page_loads(self):
        response = self.client.get('/mentorlar/')
        self.assertEqual(response.status_code, 200)

    def test_ielts_page_loads(self):
        response = self.client.get('/kurs/ielts/')
        self.assertEqual(response.status_code, 200)

    def test_sat_page_loads(self):
        response = self.client.get('/kurs/sat/')
        self.assertEqual(response.status_code, 200)

    def test_free_darslar_page_loads(self):
        response = self.client.get('/free-darslar/')
        self.assertEqual(response.status_code, 200)

    def test_kirish_page_loads(self):
        response = self.client.get('/kirish/')
        self.assertEqual(response.status_code, 200)

    def test_mentor_royxat_page_loads(self):
        response = self.client.get('/mentor/royxat/')
        self.assertEqual(response.status_code, 200)

    def test_student_royxat_page_loads(self):
        response = self.client.get('/student/royxat/')
        self.assertEqual(response.status_code, 200)


class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_with_wrong_credentials(self):
        response = self.client.post('/kirish/', {
            'username': 'notexist',
            'password': 'wrongpass'
        })
        # Login muvaffaqiyatsiz — sahifada qoladi
        self.assertEqual(response.status_code, 200)

    def test_protected_profile_redirects(self):
        # Login qilinmagan holda profil sahifasi redirect qilishi kerak
        response = self.client.get('/mentor/profil/1/')
        self.assertIn(response.status_code, [302, 404])


class TranslationsTest(TestCase):
    def test_translations_json_exists(self):
        import os
        from django.conf import settings
        path = os.path.join(settings.BASE_DIR, 'static', 'translations.json')
        self.assertTrue(os.path.exists(path), "translations.json topilmadi")

    def test_translations_has_all_languages(self):
        import json, os
        from django.conf import settings
        path = os.path.join(settings.BASE_DIR, 'static', 'translations.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn('uz', data)
        self.assertIn('en', data)
        self.assertIn('ru', data)

    def test_translations_key_counts_match(self):
        import json, os
        from django.conf import settings
        path = os.path.join(settings.BASE_DIR, 'static', 'translations.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        uz_keys = set(data['uz'].keys())
        en_keys = set(data['en'].keys())
        ru_keys = set(data['ru'].keys())
        missing_en = uz_keys - en_keys
        missing_ru = uz_keys - ru_keys
        self.assertEqual(len(missing_en), 0, f"EN da yetishmayotgan kalitlar: {missing_en}")
        self.assertEqual(len(missing_ru), 0, f"RU da yetishmayotgan kalitlar: {missing_ru}")