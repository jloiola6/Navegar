from django.test import TestCase, Client

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)