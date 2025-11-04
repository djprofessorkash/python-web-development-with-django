from django.urls import path, include
from rest_framework import routers
from .api_views import MovieViewSet, ReviewViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"genres", GenreViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]