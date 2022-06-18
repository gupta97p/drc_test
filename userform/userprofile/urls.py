from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='register')
router.register(r'create', RegisterViewSet, basename='createuser')


urlpatterns = [
    path('', include(router.urls)),
    path('verify/<int:pk>', LoginViewSet.as_view({'get': 'otp'})),
    path('update/', RegisterViewSet.as_view({'patch': 'update_email'})),
]