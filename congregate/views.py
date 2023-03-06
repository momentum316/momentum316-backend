from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .custom_permissions import IsGroupMember, IsEventMember, EventCreatePermission, ActivityCreatePermission, ActivityUpdateDestroy, PendingActivityPermission, VotingPermission, UploadCreatePermission, UploadPermission
from .models import User, Group, Event, Activity, PendingActivity, Vote, Upload
from .serializers import UserSerializer, GroupSerializer, EventSerializer, ActivitySerializer, PendingActivitySerializer, VoteSerializer, UploadSerializer

from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

import json
import random

# Create your views here.


@csrf_exempt
def GoogleLogin(request):
    data = json.loads(request.body)
    email = data.get('email', None)
    username = data.get('username', None)
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    avatar = data.get('avatar', None)

    if User.objects.filter(email=email).exists():
        user = authenticate(request, username=email)
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        # create a response with user and token data
        response_data = {
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar': user.avatarURL
            },
        }
        response_data['token'] = token.key
        return JsonResponse(response_data)
    else:
        if username is None:
            random_num = random.randint(1, 99999)
            username = 'Congregate' + str(random_num)

        i = 1
        while User.objects.filter(username=username).exists():
            new_name = f'{username}{i}'
            i += 1
            username = new_name

        user = User.objects.create(username=username, email=email)

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if avatar is not None:
            user.avatarURL = avatar

        user.save()

        user = authenticate(request, username=email)
        login(request, user, backend='config.auth_backend.EmailBackend')

        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            'user': {
                'id': str(user.id),
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar': user.avatarURL
            },
        }
        response_data['token'] = token.key
        return JsonResponse(response_data)

'''
no longer need, will wait for any bug reports from front end
'''
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
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'user with this username already exists'}, status=409)

        # Create and save the new user
        user = User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email)
        user.save()

        return redirect(f'/{user.email}/home/', status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


class UserHome(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserProfile(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserOpenVote(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        group_ids = user.user_groups.values_list('id', flat=True)
        return Event.objects.filter(group__id__in=group_ids, voting=True, decided=False).exclude(event_voter=user)


class CreateGroup(CreateAPIView):
    serializer_class = GroupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save(admin=self.request.user)
        group.members.add(self.request.user)
        return Response(serializer.data, status=201)


class UserGroup(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'username'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.user_groups.all()


class GroupHome(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'
    permission_classes = [IsGroupMember]

    def get_queryset(self):
        return Group.objects.filter(id=self.kwargs['group_id'])

    def partial_update(self, request, *args, **kwargs):
        group = self.get_object()
        if 'username' in request.data:
            user = User.objects.get(username=request.data['username'])
            group.members.add(user)
        serializer = self.get_serializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AddGroup(UpdateAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        return Group.objects.filter(id=self.kwargs['group_id'])

    def partial_update(self, request, *args, **kwargs):
        group = self.get_object()
        if 'username' in request.data:
            user = User.objects.get(username=request.data['username'])
            group.members.add(user)

            activities = Activity.objects.filter(event__group=group)
            for activity in activities:
                vote, created = Vote.objects.get_or_create(activity=activity, voter=user)

        serializer = self.get_serializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({'message': f'{user} has joined {group}'}, status=200)


class LeaveGroup(UpdateAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        return Group.objects.filter(id=self.kwargs['group_id'])

    def partial_update(self, request, *args, **kwargs):
        group = self.get_object()
        if 'username' in request.data:
            user = User.objects.get(username=request.data['username'])
            group.members.remove(user)
        serializer = self.get_serializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({'message': f'{user} has left the group'}, status=200)


class EventHome(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsEventMember]

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['event_id'])


'''
no longer needed, will wait for any bug reports from front end
'''
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


class CreateEvent(CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [EventCreatePermission]

    def post(self, request):
        group = Group.objects.get(id=request.data.get('group_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(group=group)
        return Response(serializer.data, status=201)


'''
no longer needed, will wait for any bug reports from front end
'''
def add_user_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        group_id = data.get('group_id', None)

        # Look up user and group
        user = User.objects.get(username=username)
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


'''
no longer needed, will wait for any bug reports from front end
'''
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
        creator = User.objects.get(username=username)
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


class CreateActivity(CreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [ActivityCreatePermission]

    def post(self, request):
        event = Event.objects.get(id=request.data.get('event_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activity = serializer.save(event=event, creator=request.user)

        group = event.group
        for member in group.members.all():
            vote = Vote.objects.create(voter=member, activity=activity)
            vote.save()

        return Response(serializer.data, status=201)


class ActivityUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [ActivityUpdateDestroy]
    lookup_url_kwarg = 'activity_id'

    def get_queryset(self):
        return Activity.objects.filter(id=self.kwargs['activity_id'])

    def partial_update(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=self.kwargs['activity_id'])
        self.check_object_permissions(request, activity)
        if 'username' in request.data:
            user = User.objects.get(username=request.data['username'])
            activity.attendees.add(user)
        serializer = self.get_serializer(activity, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class Voting(RetrieveUpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [VotingPermission]
    lookup_url_kwarg = 'vote_id'

    def get_queryset(self):
        return Vote.objects.filter(id=self.kwargs['vote_id'])


@csrf_exempt
def submit_vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        event_id = data.get('event_id', None)

        # Look up user and event
        user = User.objects.get(username=username)
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
            event_acts = Activity.objects.filter(event=event).annotate(total_votes=Sum('votes__vote')).order_by('-total_votes', '?')

            winning_activity = event_acts[0]
            winning_activity.is_winner = True
            winning_activity.save()

            event.decided = True
            event.save()

        return redirect(f'/event/{event_id}', status=201)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


class CreatePendingActivity(CreateAPIView):
    serializer_class = PendingActivitySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=self.request.user)
        return Response(serializer.data, status=201)


class PendingActivityUpdate(RetrieveUpdateDestroyAPIView):
    queryset = PendingActivity.objects.all()
    serializer_class = PendingActivitySerializer
    permission_classes = [PendingActivityPermission]
    lookup_url_kwarg = 'pending_activity_id'

    def get_queryset(self):
        queryset = PendingActivity.objects.filter(id=self.kwargs['pending_activity_id'])
        return queryset


class CreateUpload(CreateAPIView):
    serializer_class = UploadSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [UploadCreatePermission]

    def post(self, request):
        if 'group_id' in request.data:
            group = Group.objects.get(id=request.data.get('group_id'))
        if 'activity_id' in request.data:
            activity = Activity.objects.get(id=request.data.get('activity_id'))
        if 'description' in request.data:
            description = request.POST.get('description')
        images = request.FILES.getlist('image')
        files = request.FILES.getlist('file')

        for image in images:
            pic = Upload(owner=self.request.user, image=image)
            if activity:
                pic.activity = activity
            if group:
                pic.group = group
            if description:
                pic.description = description
            pic.save()
        for fil3 in files:
            obj = Upload(owner=self.request.user, file=fil3)
            if activity:
                obj.activity = activity
            if group:
                obj.group = group
            if description:
                obj.description = description
            obj.save()
        return JsonResponse({'message': 'Upload successful'}, status=201)


class UploadView(RetrieveUpdateDestroyAPIView):
    serializer_class = UploadSerializer
    lookup_url_kwarg = 'upload_id'
    permission_classes = [UploadPermission]

    def get_queryset(self):
        return Upload.objects.filter(id=self.kwargs['upload_id'])
