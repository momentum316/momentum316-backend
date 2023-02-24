from django.urls import path, re_path
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('google/login', views.login_with_google, name='google_login'),
    path('google/authenticate', views.authenticate_with_google, name='google_authenticate'),
    path('', views.testview, name='test'),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login1'),
    path('register/', RegisterView.as_view()),
    path('register_new', views.new_user, name='registration'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('<slug:username>/home/', views.UserHome.as_view(), name='home'),
    path('<slug:username>/groups/', views.UserGroup.as_view(), name='user_groups'),
    path('group/<int:group_id>', views.GroupHome.as_view(), name='group_home'),
    path('new/event/', views.new_event, name='new_event'),
    path('event/<int:event_id>', views.EventHome.as_view(), name='event_home'),
    path('add-user-group/', views.add_user_group, name='add_user_group'),
    path('new/activity/', views.new_activity, name='new_event'),
]
