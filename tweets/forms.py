from django import forms
from django.conf import settings
from .models import Tweet

MAX_LENGTH = settings.MAX_TWEET_LENGTH

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("Too long")
        return content
