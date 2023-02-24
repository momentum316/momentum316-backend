from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .models import User, CongregateUser, Group, Event, Activity
# Activity
from .serializers import CongregateUserSerializer, GroupSerializer, EventSerializer, ActivitySerializer
from rest_framework import response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
# ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
import json, random, string


from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from django.contrib.auth import authenticate, login


# Create your views here.


def login_with_google(request):
    # Generate a random state string
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    # Set up the Google OAuth2 flow
    flow = Flow.from_client_secrets_file(
        '/Users/jerome/Momentum/Homework/congregate/client_secret_870515678880-to68ob9lpvub6iiqrrlvasljoebp7jvs.apps.googleusercontent.com.json',
        scopes=['openid', 'email', 'profile', 'https://www.googleapis.com/auth/calendar']
    )
    flow.redirect_uri = 'http://localhost:8000/google/authenticate'

    # Generate the Google OAuth2 authorization URL
    authorization_url, state = flow.authorization_url(
        prompt='consent',
        state=state,
        access_type='offline',
    )

    # Save the state value to the session for later validation
    request.session['google_oauth2_state'] = state

    # Redirect the user to the Google OAuth2 authorization URL
    return redirect(authorization_url)


def authenticate_with_google(request):
    # Get the Google OAuth2 authorization code from the request
    authorization_code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    if authorization_code is None:
        return HttpResponseBadRequest('Missing authorization code')
    # Verify that the state parameter matches the one saved in the session
    if state != request.session.get('google_oauth2_state', None):
        return HttpResponseBadRequest('Invalid state parameter')

    # Set up the Google OAuth2 flow
    flow = Flow.from_client_secrets_file(
        '/Users/jerome/Momentum/Homework/congregate/client_secret_870515678880-to68ob9lpvub6iiqrrlvasljoebp7jvs.apps.googleusercontent.com.json',
        scopes=['openid', 'email', 'profile', 'https://www.googleapis.com/auth/calendar']
    )
    flow.redirect_uri = 'https://congregate.onrender.com/jcox/home'

    # Exchange the Google OAuth2 authorization code for an access token and refresh token
    flow.fetch_token(authorization_response=request.get_full_path())

    # Get the user's Google profile information
    credentials = flow.credentials
    google_profile = build('oauth2', 'v2', credentials=credentials).userinfo().get().execute()

    # Authenticate the user with Django's authentication system
    user = authenticate(request, username=google_profile['email'], password=None)
    if user is None:
        # If the user doesn't exist in the Django database, create a new user
        user = User.objects.create_user(
            username=google_profile['email'],
            email=google_profile['email'],
            password=None
        )
    login(request, user)

    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }

    # Redirect the user to the home page
    return redirect(
        '/',
        token='token.key',
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
    )


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
    callback_url = 'http://localhost:8000/accounts/google/login/callback/'
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
        user = get_object_or_404(CongregateUser, username=self.kwargs['username'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect(f'/{user.username}/groups/', status=201)


class GroupHome(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'


class EventHome(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        queryset = Event.objects.filter(id=self.kwargs['event_id'])
        return queryset


@csrf_exempt
def new_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', None)
        group_id = data.get('group_id', None)
        voting = data.get('voting', None)
        date = data.get('date', None)
        vote_closing_time = data.get('vote_closing_time', None)

        # Create and save the new event
        group = Group.objects.get(id=group_id)
        event = Event.objects.create(title=title, group=group, voting=voting, date=date, vote_closing_time=vote_closing_time)
        event.save()

        return JsonResponse({'event': {'id': event.id, 'title': event.title, 'voting': event.voting, 'date': event.date, 'vote_closing_time': event.vote_closing_time}}, status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


@csrf_exempt
def add_user_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        group_id = data.get('group_id', None)

        # Look up user and group
        user = CongregateUser.objects.get(username=username)
        group = Group.objects.get(id=group_id)

        # Check if user is already a member of the group
        if user in group.members.all():
            return JsonResponse({'error': f'{username} is already a member of the group'}, status=409)

        # Add user to group members list
        group.members.add(user)

        return redirect(f'/group/{group_id}', status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


@csrf_exempt
def new_activity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', None)
        event_id = data.get('event_id', None)
        description = data.get('description', None)
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)

        # Create and save the new event
        event = Event.objects.get(id=event_id)
        activity = Activity.objects.create(title=title, event=event, description=description, start_time=start_time, end_time=end_time)
        activity.save()

        return JsonResponse({'activity': {'id': activity.id, 'title': activity.title, 'description': activity.description, 'start_time': activity.start_time, 'end_time': activity.end_time}}, status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)
