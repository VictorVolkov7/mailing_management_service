from django.urls import path

from users.apps import UserConfig
from users.views import LoginView, LogoutView, UserUpdateView, UserCreateView, VerifiedSentView, verify_email, \
    UserListView, toggle_ban_activity

app_name = UserConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('register/verified/', VerifiedSentView.as_view(), name='verified'),
    path('verify_email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('ban_activity/<int:pk>', toggle_ban_activity, name='user_ban'),
]
