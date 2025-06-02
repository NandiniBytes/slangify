from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlangViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'slangs', SlangViewSet, basename='slang')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]