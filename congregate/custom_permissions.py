from rest_framework.permissions import BasePermission


class IsGroupMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user is obj.admin

        return obj in request.user.user_groups.all()
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # # Instance must have an attribute named `owner`.
        # return obj.owner == request.user



# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS

# class ExampleView(APIView):
#     permission_classes = [IsAuthenticated|ReadOnly]

#     def get(self, request, format=None):
#         content = {
#             'status': 'request was permitted'
#         }
#         return Response(content)

#         def get_object(self):
#     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
#     self.check_object_permissions(self.request, obj)
#     return obj