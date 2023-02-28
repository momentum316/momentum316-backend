from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import CongregateUser, Group, Event, Activity, Vote
from .serializers import CongregateUserSerializer, GroupSerializer, EventSerializer, ActivitySerializer, VoteSerializer, DecidedEventSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView, ListAPIView, UpdateAPIView
import json
from rest_framework.authtoken.models import Token

# Create your views here.

@csrf_exempt
def logintest(request):
    data = json.loads(request.body)
    email = data.get('email', None)

    user = authenticate(request, username=email)
    if user is not None:
        login(request, user)
        return user


@csrf_exempt
def GoogleLogin(request):
    data = json.loads(request.body)
    email = data.get('email', None)

    user = authenticate(request, username=email)
    if user is not None:
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        # create a response with user and token data
        response_data = {
            'user': {
                'id': str(user.id),
                'email': user.email,
            },
        }
        response_data['token'] = token.key
        return JsonResponse(response_data)

    # return an error response if authentication fails
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@csrf_exempt
def new_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)

        # Validate required fields are present
        if not all([first_name, last_name, email]):
            return JsonResponse({'error': 'username, first_name, last_name, and email are required fields'}, status=400)

        # Authenticate user with email
        user = authenticate(request, email=email)
        if user is not None:
            login(request, user)
            return redirect(f'/{user.username}/home/', status=302)

        # Check if the user already exists
        if CongregateUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'user with this username already exists'}, status=409)

        # Create and save the new user
        user = CongregateUser.objects.create(username=email, first_name=first_name, last_name=last_name, email=email)
        user.save()

        return redirect(f'/{user.email}/home/', status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


class UserHome(RetrieveUpdateAPIView):
    queryset = CongregateUser.objects.all()
    serializer_class = CongregateUserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'


@csrf_exempt
def create_group_view(request):
    data = json.loads(request.body)
    username = data.get('username', None)
    title = data.get('title', None)
    user = get_object_or_404(CongregateUser, username=username)

    group = Group.objects.create(title=title, admin=user)
    group.members.add(user)
    group.save()

    return JsonResponse({'group': {'id': group.id, 'title': group.title}}, status=201)


class UserGroup(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'username'

    def get_queryset(self):
        user = get_object_or_404(CongregateUser, username=self.kwargs['username'])
        return user.user_groups.all()


class GroupHome(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        queryset = Group.objects.filter(id=self.kwargs['group_id'])
        return queryset


class EventHome(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'event_id'

    def get_serializer_class(self):
        event = self.get_object()
        if event.decided:
            return DecidedEventSerializer
        return EventSerializer

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

        # Need to add these
        # If user not found...
        # If group does not exists, throw 404

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
        username = data.get('username', None)
        description = data.get('description', None)
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)

        # Create and save the new event
        creator = CongregateUser.objects.get(username=username)
        event = Event.objects.get(id=event_id)
        activity = Activity.objects.create(title=title, event=event, creator=creator, description=description, start_time=start_time, end_time=end_time)
        activity.save()

        group = event.group
        for member in group.members.all():
            vote = Vote.objects.create(voter=member, activity=activity)
            vote.save()

        return JsonResponse({'activity': {'id': activity.id, 'title': activity.title, 'description': activity.description, 'start_time': activity.start_time, 'end_time': activity.end_time}}, status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


class ActivityUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    lookup_url_kwarg = 'activity_id'

    def get_queryset(self):
        queryset = Activity.objects.filter(id=self.kwargs['activity_id'])
        return queryset


class Voting(UpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_url_kwarg = 'vote_id'

    def get_queryset(self):
        vote = Vote.objects.get(id=self.kwargs['vote_id'])
        if self.request.data.get('username') != vote.voter.username:
            return redirect(self.request.META.get('HTTP_REFERER'))
        queryset = Vote.objects.filter(id=self.kwargs['vote_id'])
        return queryset


@csrf_exempt
def submit_vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        event_id = data.get('event_id', None)

        # Look up user and event
        user = CongregateUser.objects.get(username=username)
        event = Event.objects.get(id=event_id)

        # Check if user has already submitted votes
        if user in event.event_voter.all():
            return JsonResponse({'error': f'{username} has already voted'}, status=409)

        # Need to add these
        # If user not found...
        # If event does not exists, throw 404

        # Add user to event.voted list
        event.event_voter.add(user)

        group = event.group

        if group.members.count() <= event.event_voter.count():
            event.decided = True
            event.save()
            return redirect(f'/event-winner/{event_id}')

        return redirect(f'/event/{event_id}', status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


class DecideEvent(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = DecidedEventSerializer
    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        event = Event.objects.get(id=self.kwargs['event_id'])
        event.decided = True
        return Event.objects.filter(id=self.kwargs['event_id'])
