from django.shortcuts import render, get_object_or_404
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .models import CongregateUser
# Group, Event, EventOption
from .serializers import CongregateUserSerializer
# EventSerializer, EventOptionSerializer
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
    queryset = CongregateUser.objects.all()
    serializer_class = CongregateUserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'


# class GroupHome(RetrieveUpdateDestroyAPIView):
#     serializer_class = GroupSerializer

#     def get_queryset(self):
#         return 