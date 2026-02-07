from django.test import Client, TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    """Tests pour la vue d'accueil."""

    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        """Test que la page d'accueil retourne un code 200."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        """Test que le bon template est utilisé pour la page d'accueil."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/index.html")
