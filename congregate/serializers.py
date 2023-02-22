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
    model = Group
    fields = '__all__'


class EventSerializer(ModelSerializer):
    model = Event
    fields = '__all__'


class EventOptionSerializer(ModelSerializer):
    model = EventOption
    fields = '__all__'
