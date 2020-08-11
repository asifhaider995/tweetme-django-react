from rest_framework import serializers
from django.conf import settings
from .models import Tweet

MAX_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTIONS = settings.TWEET_ACTIONS

class TweetActionSerializer(serializers.Serializer):
    """
        Tweet Action Serializer Class
        Serializes tweet liking, unliking, retweeting
    """
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Likes " -> "likes"
        if value not in TWEET_ACTIONS:
            raise serializers.ValidationError("Invalid action")
        return value

class TweetCreateSerializer(serializers.ModelSerializer):
    """
        Serializer class for creating tweets
        Handles post method, so it needs validation
        Serializes username, content, date_created
        Validation method validates if content length
        is greater than limit
    """
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'date_created' ]

    def validate_content(self, value):
        if(len(value) > MAX_LENGTH):
            raise serializers.ValidationError("This tweet is too long")
        return value

    def get_likes(self, obj):
        return obj.likes.count()


class TweetUpdateSerializer(serializers.ModelSerializer):
    """
        Serializer class for updating tweets
        Handles put method, so it needs validation
        Serializes username, content, date_created
        Validation method validates if content length
        is greater than limit
    """
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'date_created' ]

    def validate_content(self, value):
        if(len(value) > MAX_LENGTH):
            raise serializers.ValidationError("This tweet is too long")
        return value


class TweetSerializer(serializers.ModelSerializer):
    """
        Read Only Serializer class
    """
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'date_created', 'likes', 'parent']

    def get_likes(self, obj):
        return obj.likes.count()
