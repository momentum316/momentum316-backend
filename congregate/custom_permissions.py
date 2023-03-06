from rest_framework.permissions import BasePermission
from .models import Group, Event, Activity


class IsGroupMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user is obj.admin

        return obj in request.user.user_groups.all()


class IsEventMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user is obj.group.admin

        return request.user in obj.group.members.all()


class EventCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            group = Group.objects.get(id=request.data['group_id'])
            return request.user in group.members.all()


class ActivityUpdateDestroy(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return request.user == obj.creator or request.user == obj.event.group.admin

        return True


class ActivityCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            event = Event.objects.get(id=request.data['event_id'])
            return request.user in event.group.members.all()


class PendingActivityPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class VotingPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.voter


class UploadCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if 'group_id' in request.data:
                group = Group.objects.get(id=request.data['group_id'])
                if 'activity_id' in request.data:
                    activity = Activity.objects.get(id=request.data['activity_id'])
                    return request.user == activity.creator or request.user == group.admin
                return request.user in group.members.all()

            return True


class UploadPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.group:
            return request.user == obj.owner or request.user == obj.group.admin

        return request.user == obj.owner
