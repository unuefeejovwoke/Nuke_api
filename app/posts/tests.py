from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Post

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            title="A good title",
            body="Nice body content",
        )

    def test_post_model(self):
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.title, "A good title")
        self.assertEqual(self.post.body, "Nice body content")
        self.assertEqual(str(self.post), "A good title")

    def test_reading_time(self):
        # Adjust the expected reading time based on the content and words-per-minute rate
        expected_reading_time_minutes = 1
        self.assertEqual(self.post.reading_time_minutes(), expected_reading_time_minutes)

    def test_display_reading_time(self):
        # Adjust the expected reading time based on the content and words-per-minute rate
        expected_display = "1 min read"
        self.assertEqual(self.post.display_reading_time(), expected_display)
