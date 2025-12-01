from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Note
from api.serializers import NoteSerializer


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class NoteSerializerTests(APITestCase):
    def test_title_required_and_trimmed(self):
        serializer = NoteSerializer(data={"title": "  "})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

        serializer_ok = NoteSerializer(data={"title": "  Hello  "})
        self.assertTrue(serializer_ok.is_valid())
        self.assertEqual(serializer_ok.validated_data["title"], "Hello")


class NoteAPITests(APITestCase):
    def setUp(self):
        Note.objects.create(title="Alpha", content="a")
        Note.objects.create(title="Beta", content="b", is_archived=True)
        Note.objects.create(title="Gamma Note", content="c")

    def test_list_notes_with_search_and_pagination(self):
        url = "/api/notes/?search=note&page=1&size=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include "Gamma Note" only when searching "note"
        titles = [n["title"] for n in response.data["results"]]
        self.assertIn("Gamma Note", titles)

    def test_create_note(self):
        url = "/api/notes/"
        payload = {"title": "New Item", "content": "Body"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Item")
