from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from problems.views import TagViewSet, ProblemViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('problems', ProblemViewSet, basename='problem')

urlpatterns = router.urls
