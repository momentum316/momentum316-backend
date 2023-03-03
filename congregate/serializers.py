from django.db.models import Sum
from rest_framework.serializers import ModelSerializer, SerializerMethodField, SlugRelatedField
from .models import User, Group, Event, Activity, PendingActivity, Vote


class VoteSerializer(ModelSerializer):
    activity = SlugRelatedField(slug_field='title', read_only=True)
    voter = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Vote
        fields = (
            'id',
            'voter',
            'activity',
            'vote',
        )


class PendingActivitySerializer(ModelSerializer):
    creator = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = PendingActivity
        fields = '__all__'


class ActivitySerializer(ModelSerializer):
    event = SlugRelatedField(slug_field='title', read_only=True)
    creator = SlugRelatedField(slug_field='username', read_only=True)
    vote_list = VoteSerializer(many=True, source='votes', read_only=True)
    total_votes = SerializerMethodField('get_votes_tally')
    attendees = SlugRelatedField(slug_field='username', many=True, read_only=True)

    def get_votes_tally(self, obj):
        return obj.votes.aggregate(total_votes=Sum('vote'))['total_votes']

    class Meta:
        model = Activity
        fields = (
            'id',
            'title',
            'event',
            'creator',
            'description',
            'location',
            'start_time',
            'end_time',
            'vote_list',
            'total_votes',
            'is_winner',
            'attendees',
        )


class EventSerializer(ModelSerializer):
    group = SlugRelatedField(slug_field='title', read_only=True)
    activity_list = SerializerMethodField()

    def get_activity_list(self, obj):
        activities = obj.activities.distinct()
        serializer = ActivitySerializer(instance=activities, many=True)
        return serializer.data

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'voting',
            'date',
            'activity_list',
            'group',
            'vote_closing_time',
            'decided',
        )


# Is this necessary?
class DecidedEventSerializer(ModelSerializer):
    group = SlugRelatedField(slug_field='title', read_only=True)
    activity_list = SerializerMethodField('get_activity_list')

    def get_activity_list(self, obj):
        activities = obj.activities.all().order_by('-votes')
        serializer = ActivitySerializer(activities, many=True)
        return serializer.data

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'voting',
            'date',
            'activity_list',
            'group',
            'vote_closing_time',
            'decided',
        )


class GroupSerializer(ModelSerializer):
    members = SlugRelatedField(slug_field='username', many=True, read_only=True)
    admin = SlugRelatedField(slug_field='username', read_only=True)
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


class UserSerializer(ModelSerializer):
    group_list = GroupSerializer(many=True, source='user_groups', read_only=True)
    pending_activities = SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatarURL',
            'pending_activities',
            'group_list',
        )
