from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .custom_permissions import IsUser, IsGroupMember, IsEventMember, EventCreatePermission, ActivityCreatePermission, ActivityUpdateDestroy, PendingActivityPermission, VotingPermission, UploadCreatePermission, UploadPermission
from .models import User, Group, Event, Activity, PendingActivity, Vote, Upload
from .serializers import UserSerializer, GroupSerializer, EventSerializer, ActivitySerializer, PendingActivitySerializer, VoteSerializer, UploadSerializer

from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
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


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({"message": "Logout successful"})
        else:
            return Response({"message": "User is not logged in"})


class UserHome(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsUser]


class UserProfile(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.kwargs['username'])
    #     return user


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


class AttendEvent(UpdateAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsEventMember]

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['event_id'])

    def partial_update(self, request, *args, **kwargs):
        event = self.get_object()
        self.check_object_permissions(request, event)
        if 'username' in request.data:
            user = User.objects.get(username=request.data['username'])
            event.attendees.add(user)
        serializer = self.get_serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({'message': f'{user} is attending this event'}, status=200)


class RemoveAttendEvent(UpdateAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsEventMember]

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['event_id'])

    def partial_update(self, request, *args, **kwargs):
        event = self.get_object()
        self.check_object_permissions(request, event)
        if 'username' in request.data:
            user = User.objects.get(username=request.data['username'])
            event.attendees.remove(user)
        serializer = self.get_serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({'message': f'{user} is no longer attending this event'}, status=200)


class CreateEvent(CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [EventCreatePermission]

    def post(self, request):
        group = Group.objects.get(id=request.data.get('group_id'))
        voting = request.data['voting']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not voting:
            serializer.save(group=group, decided=True)
        else:
            serializer.save(group=group)
        return Response(serializer.data, status=201)


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
