from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .models import CongregateUser, Group
# Event, EventOption
from .serializers import CongregateUserSerializer, GroupSerializer
# EventSerializer, EventOptionSerializer
from rest_framework import response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
# ListAPIView, DestroyAPIView, UpdateAPIView
import json

# Create your views here.


def testview(request):
    return render(request, 'test.html', {})


@csrf_exempt
def new_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)

        # Validate required fields are present
        if not all([username, first_name, last_name, email]):
            return JsonResponse({'error': 'username, first_name, last_name, and email are required fields'}, status=400)

        if CongregateUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'user is already registered with this email'}, status=409)

        # Check if the user already exists
        if CongregateUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'user with this username already exists'}, status=409)

        # Create and save the new user
        user = CongregateUser.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
        user.save()

        return redirect(f'/{user.username}/home/', status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/callback/'
    client_class = OAuth2Client


class UserHome(RetrieveUpdateDestroyAPIView):
    queryset = CongregateUser.objects.all()
    serializer_class = CongregateUserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'


class UserGroup(ListCreateAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'username'

    def get_queryset(self):
        user = get_object_or_404(CongregateUser, username=self.kwargs['username'])
        return user.user_groups.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect(f'/{user.username}/groups/', status=201)


# class GroupHome(RetrieveUpdateDestroyAPIView):
#     serializer_class = GroupSerializer

#     def get_queryset(self):
#         return