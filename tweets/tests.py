from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Tweet
from rest_framework.test import APIClient
# Create your tests here.

User = get_user_model()

class TweetTestCase(TestCase):
    """
        Test case for Tweets
    """
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='&66%')
        self.userEd = User.objects.create_user(username='ed', password='&66%')
        tweet = Tweet.objects.create(content='first Tweet', user=self.user)
        tweet = Tweet.objects.create(content='first as Tweet', user=self.user)
        tweet = Tweet.objects.create(content='first not Tweet', user=self.userEd)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet = Tweet.objects.create(content='second Tweet', user=self.user)
        self.assertEqual(tweet.id, 4)
        self.assertEqual(tweet.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='&66%')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 1, "action": 'like'})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        print(response.json())

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 1, "action": 'like'})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action/", {"id": 1, "action": 'unlike'})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
        print(response.json())

    def test_action_retweet(self):
        client = self.get_client()
        current_count = self.currentCount
        response = client.post("/api/tweets/action/", {"id": 1, "action": 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = (response.json())
        new_tweet_id = data.get("id")
        self.assertNotEqual(1, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_create(self):
        request_data = {"content": "Another Tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')
        self.assertEqual(self.currentCount + 1, new_tweet_id)

    def test_tweet_detail(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 1)
        response = client.get("/api/tweets/2/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 2)
        response = client.get("/api/tweets/6/")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, None)

    def test_tweet_delete(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        response = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response.status_code, 401)
