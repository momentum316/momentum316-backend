from django.urls import path
from . import views

urlpatterns = [
    path('login', views.GoogleLogin, name='login'),
    path('register', views.new_user, name='registration'),
    path('<username>/home/', views.UserHome.as_view(), name='home'),
    path('<username>/profile/', views.UserProfile.as_view(), name='profile'),
    path('<username>/groups/', views.UserGroup.as_view(), name='user_groups'),
    path('my-open-votes', views.UserOpenVote.as_view(), name='user_open_vote'),
    path('new/group/', views.CreateGroup.as_view(), name='new_group'),
    path('group/<int:group_id>', views.GroupHome.as_view(), name='group_home'),
    path('join/<int:group_id>', views.AddGroup.as_view(), name='join_group'),
    path('leave/<int:group_id>', views.LeaveGroup.as_view(), name='leave_group'),
    path('new/event/', views.CreateEvent.as_view(), name='new_event'),
    path('event/<int:event_id>', views.EventHome.as_view(), name='event_home'),
    path('new/activity/', views.CreateActivity.as_view(), name='new_activity'),
    path('activity/<int:activity_id>', views.ActivityUpdate.as_view(), name='activity_update'),
    path('vote/<int:vote_id>', views.Voting.as_view(), name='vote'),
    path('submit-vote/', views.submit_vote, name='submit_vote'),
    path('new/pending-activity/', views.CreatePendingActivity.as_view(), name='new_pending_activity'),
    path('pending/<int:pending_activity_id>', views.PendingActivityUpdate.as_view(), name='pending_activity_update'),
    path('new/upload/', views.CreateUpload.as_view(), name='new_upload'),
    path('upload/<int:upload_id>', views.UploadView.as_view(), name='upload_view'),
]
