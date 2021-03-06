from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Profile

User = get_user_model()

class ProfileTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="qwe", password="strong123")
        self.user_1 = User.objects.create_user(username="rty", password="strong1234")

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="strong123")
        return client

    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_following(self):
        first = self.user
        second = self.user_1
        first.profile.followers.add(second) # добавляю подписчика
        second_user_following_whom = second.following.all()
        qs = second_user_following_whom.filter(user=first) # проверяю что подписчик появился
        self.assertTrue(qs.exists())

        first_user_following_no_one = first.following.all() # проверяю что новый пользователь ни на кого не подписан
        self.assertFalse(first_user_following_no_one.exists())

    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.user_1.username}/follow", {"action": "follow"})
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 1)

    def test_unfollow_api_endpoint(self):
        first = self.user
        second = self.user_1
        first.profile.followers.add(second)
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.user_1.username}/follow", {"action": "unfollow"})
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)

    def test_cannot_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.user.username}/follow", {"action": "follow"})
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)