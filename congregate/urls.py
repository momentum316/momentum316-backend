from django.urls import path
from . import views

urlpatterns = [
    path('', views.testview, name='test'),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('<slug:username>/home/', views.UserHome.as_view(), name='home'),
]
