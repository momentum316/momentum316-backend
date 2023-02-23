from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CongregateUser, Group, Event, Activity


class ActivitySerializer(ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'


class EventSerializer(ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='title', read_only=True)
    activity_list = ActivitySerializer(many=True, source='options', read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'group',
            'voting',
            'start_time',
            'vote_closing_time',
            'activity_list',
        )


class GroupSerializer(ModelSerializer):
    members = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)
    admin = serializers.SlugRelatedField(slug_field='username', read_only=True)
    event_list = EventSerializer(many=True, source='events', read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'members',
            'admin',
            'event_list',
        )


class CongregateUserSerializer(ModelSerializer):
    group_list = GroupSerializer(many=True, source='user_groups', read_only=True)

    class Meta:
        model = CongregateUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'group_list',
        )


