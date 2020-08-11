from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', {})

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
class TweetUpdateView(UpdateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    serializer = TweetSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, id, *args, **kwargs):
    queryset = Tweet.objects.filter(id=id)
    if queryset.exists():
        serializer = TweetSerializer(queryset.first())
        return Response(serializer.data, status=200)
    return Response({},status=404)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, id, *args, **kwargs):
    queryset = Tweet.objects.filter(id=id)
    if not queryset.exists():
        return Response({}, status=404)
    queryset = queryset.filter(user=request.user)
    # Is the current user the creator of the Tweet
    if not queryset.exists():
        return Response({"message": "You are not Authorized"}, status=401)
    obj = queryset.first()
    obj.delete()
    return Response({"message": "Tweet deleted"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """
        Tweet action options are
            - like
            - unlike
            - retweet
        Dependency:
            - id
    """
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        id = data.get("id")
        action = data.get("action")
        rt_content = data.get("content")
        queryset = Tweet.objects.filter(id=id)
        if not queryset.exists():
            return Response({}, status=404)
        obj = queryset.first()
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            retweet_obj = Tweet.objects.create(user=request.user, parent=obj, content=rt_content)
            serializer = TweetSerializer(retweet_obj)
            return Response(serializer.data, status=201)

    return Response({"message": "Action Complete"}, status=200)



##################################################################
####################  Pure Django Views ##########################
##################################################################


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    else:
        form = TweetForm(request.POST or None)
        next_url = request.POST.get('next') or None
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = requet.user or None
            obj.save()
            if request.is_ajax():
                return JsonResponse(obj.serialize(), status=201)
            if next_url != None and is_safe_url(next_url, settings.ALLOWED_HOSTS):
                return redirect(next_url)
        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
        return render(request, 'components/forms.html', context={'form': form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweet_list = [i.serialize() for i in queryset]
    data = {
        "isUser"   : False,
        "response" : tweet_list
    }
    return JsonResponse(data, status=200)

def tweet_detail_view_pure_django(request, id, *args, **kwargs):
    """
    REST API VIEW
    """
    obj = get_object_or_404(Tweet, pk=id)
    data = {
        'id' : id,
        'content': obj.content,
        'date' : obj.date_created
    }
    return JsonResponse(data, status=200) #JSON Dump ContentType: 'application/json'
