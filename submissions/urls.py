from rest_framework.routers import DefaultRouter

from submissions.views import SubmissionViewSet

router = DefaultRouter()
urlpatterns = router.urls

router = DefaultRouter()

router.register('submission', SubmissionViewSet, basename='submission')