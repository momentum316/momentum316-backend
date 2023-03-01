from django.urls import path
from . import views

urlpatterns = [
    path('login', views.GoogleLogin, name='login'),
    path('register', views.new_user, name='registration'),
    path('<username>/home/', views.UserHome.as_view(), name='home'),
    path('<username>/profile/', views.UserProfile.as_view(), name='profile'),
    path('<username>/groups/', views.UserGroup.as_view(), name='user_groups'),
    path('<username>/open-votes', views.UserOpenVote.as_view(), name='user_open_vote'),
    path('new/group/', views.CreateGroup.as_view(), name='new_group'),
    path('group/<int:group_id>', views.GroupHome.as_view(), name='group_home'),
    path('new/event/', views.new_event, name='new_event'),
    path('event/<int:event_id>', views.EventHome.as_view(), name='event_home'),
    path('add-user-group/', views.add_user_group, name='add_user_group'),
    path('new/activity/', views.new_activity, name='new_event'),
    path('activity/<int:activity_id>', views.ActivityUpdate.as_view(), name='activity_update'),
    path('vote/<int:vote_id>', views.Voting.as_view(), name='vote'),
    path('submit-vote/', views.submit_vote, name='submit_vote'),
]
