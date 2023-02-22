from rest_framework.serializers import ModelSerializer
from .models import User, Group, Event, EventOption


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
        )
