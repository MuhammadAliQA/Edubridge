from django.test import TestCase, Client


class PublicPagesSmokeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EduBridge")

    def test_public_pages_load(self):
        for url in [
            "/mentorlar/",
            "/kurs/ielts/",
            "/kurs/sat/",
            "/free-darslar/",
            "/admission/",
            "/grants/",
            "/healthz/",
        ]:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 200)

