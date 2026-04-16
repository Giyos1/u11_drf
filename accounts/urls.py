from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Login → access+refresh
    TokenRefreshView,  # Refresh → yangi access
    TokenBlacklistView,  # Logout → blacklist
)
from accounts.views import AuthViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
