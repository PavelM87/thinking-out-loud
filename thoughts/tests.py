from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import response

from rest_framework.test import APIClient

from .models import Post


User = get_user_model()

class PostTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="qwe", password="strong123")
        self.user_1 = User.objects.create_user(username="rty", password="strong1234")
        Post.objects.create(content="this is new post", user=self.user)
        Post.objects.create(content="awesome post", user=self.user)
        Post.objects.create(content="this is not new post", user=self.user)
        Post.objects.create(content="this is sparta!11", user=self.user_1)
        self.currentCount = Post.objects.all().count()


    def test_user_created(self):
        self.assertEqual(self.user.username, "qwe")

    def test_post_created(self):
        post_obj = Post.objects.create(content="this is one more new post", user=self.user)
        self.assertEqual(post_obj.id, 5)
        self.assertEqual(post_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="strong123")
        return client

    def test_post_list(self):
        client = self.get_client()
        response = client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_post_list(self):
        client = self.get_client()
        response = client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_posts_related_name(self):
        user = self.user
        self.assertEqual(user.posts.count(), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/posts/action/", {"id": 1, "action": "like"}) 
        self.assertEqual(response.status_code, 200)

        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        self.assertEqual(len(response.json()), 5)

        user = self.user
        my_like_instances = user.postlike_set.count()
        self.assertEqual(my_like_instances, 1)

        my_related_likes = user.post_user.count()
        self.assertEqual(my_related_likes, my_like_instances)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/posts/action/", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)

        response = client.post("/api/posts/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)

        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)

    def test_action_repost(self):
        client = self.get_client()
        response = client.post("/api/posts/action/", {"id": 2, "action": "repost"})
        self.assertEqual(response.status_code, 201)

        data = response.json()
        new_post_id = data.get("id")
        self.assertNotEqual(2, new_post_id)
        self.assertEqual(self.currentCount + 1, new_post_id)

    def test_post_create_api(self):
        request_data = {"content": "Test post"}
        client = self.get_client()
        response = client.post("/api/posts/create/", request_data)
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        new_post_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_post_id)

    def test_post_detail_api(self):
        client = self.get_client()
        response = client.get("/api/posts/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_post_delete_api(self):
        client = self.get_client()
        response = client.delete("/api/posts/1/delete/")
        self.assertEqual(response.status_code, 200)

        client = self.get_client()
        response = client.delete("/api/posts/1/delete/")
        self.assertEqual(response.status_code, 404)

        response_incorrect = client.delete("/api/posts/4/delete/")
        self.assertEqual(response_incorrect.status_code, 401)

    


