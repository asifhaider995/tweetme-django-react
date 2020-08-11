from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    # Model name in quotes because the model definition is below this
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    # Maps to SQLite data
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=settings.MAX_TWEET_LENGTH, null=True)
    image = models.FileField(upload_to='images/', blank=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike) # Through for Timestamp of the like
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content

    @property
    def is_retweet(self):
        """ Checks if self is retweet """
        return self.parent != None

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "content": self.content,
    #         "date" : self.date_created
    #     }
