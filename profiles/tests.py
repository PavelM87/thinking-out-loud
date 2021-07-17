from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

class ProfileTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="qwe", password="strong123")
        self.user_1 = User.objects.create_user(username="rty", password="strong1234")

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
