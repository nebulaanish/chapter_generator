from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChapterViewSet


# Create a router and register the viewset
router = DefaultRouter()
router.register(r"chapters", ChapterViewSet, basename="chapter")

# Use the router's URLs in your app's URL patterns
urlpatterns = [
    path("", include(router.urls)),
]
