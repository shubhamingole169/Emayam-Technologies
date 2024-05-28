from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView, UserDetailView,
    login_page, register_page, dashboard_page, admin_page, editor_page, viewer_page, home, view_content, edit_content, api_root
)

urlpatterns = [
    path('', home, name='home'),
    path('login-page/', login_page, name='login_page'),
    path('register-page/', register_page, name='register_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('admin/', admin_page, name='admin_page'),
    path('editor/', editor_page, name='editor_page'),
    path('viewer/', viewer_page, name='viewer_page'),
    path('view-content/', view_content, name='view_content'),
    path('edit-content/', edit_content, name='edit_content'),
    path('api-root/', api_root, name='api_root'),

    # API paths
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserDetailView.as_view(), name='api_user'),
]
