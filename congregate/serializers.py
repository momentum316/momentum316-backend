from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CongregateUser, Group, Event, EventOption


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


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


class EventOptionSerializer(ModelSerializer):

    class Meta:
        model = EventOption
        fields = '__all__'
