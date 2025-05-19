from django.urls import path
from .views import RegisterView
from .views import CreateProfileView, UserProfileView, CheckRoleView, UserDetailView, UserCreateView, UserDeleteView, UserListByRoleView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/profile/create/', CreateProfileView.as_view(), name='create-profile'),
    path('auth/profile/', UserProfileView.as_view(), name='get-profile'),
    path('auth/check-role', CheckRoleView.as_view(), name='check-role'),
    path('auth/users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('auth/users/', UserCreateView.as_view(), name='user-create'),
    path('auth/users/<int:id>/delete/', UserDeleteView.as_view(), name='user-delete'),
     path('users/role/<str:role>/', UserListByRoleView.as_view(), name='user-by-role'),
]
