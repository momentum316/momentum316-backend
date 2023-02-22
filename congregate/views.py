from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .models import User
# Group, Event, EventOption
from .serializers import UserSerializer
# GroupSerializer, EventSerializer, EventOptionSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
# ListCreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView

# Create your views here.


def testview(request):
    return render(request, 'test.html', {})


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/callback/'
    client_class = OAuth2Client


class UserHome(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(username=self.request.user)
        return queryset
