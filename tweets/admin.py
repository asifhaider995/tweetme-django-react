from django.contrib import admin
from .models import Tweet, TweetLike
# Register your models here.

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


class TweetAdmin(admin.ModelAdmin):
    """
        Search filter class
        Add a search bar to Admin panel of Tweets
        Search by user and,
        Search by email and,
        Search by content

        **WARNING - Cannot use `user__username` in `list_display`
    """
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user', 'date_created']
    search_fields = ['content','user__username', 'user__email']
    date_heirrarchy = ['date_created']
    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetAdmin)
