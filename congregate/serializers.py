from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CongregateUser, Group, Event, EventOption


class CongregateUserSerializer(ModelSerializer):

    class Meta:
        model = CongregateUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
        )


class GroupSerializer(ModelSerializer):
    members = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)
    admin = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'members',
            'admin'
        )


class EventSerializer(ModelSerializer):
    model = Event
    fields = '__all__'


class EventOptionSerializer(ModelSerializer):
    model = EventOption
    fields = '__all__'
