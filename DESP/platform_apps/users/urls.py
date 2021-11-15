from django.urls import path

from .views import DESPUserView, DESPUserDetailView, RegistrationView, LoginView, TokenProfileView

urlpatterns = [
    path(r'', DESPUserView.as_view(), name="users"),
    path(r'<int:id>/', DESPUserDetailView.as_view(), name="user_details"),
    path(r'register/', RegistrationView.as_view(), name="register"),
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'token_profile/', TokenProfileView.as_view(), name="profile"),
]
