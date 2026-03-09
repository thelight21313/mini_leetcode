from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from leet_code.problems.views import TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('problems', TagViewSet, basename='problem')
