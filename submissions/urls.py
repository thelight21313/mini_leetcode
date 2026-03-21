from rest_framework.routers import DefaultRouter

from submissions.views import SubmissionViewSet

router = DefaultRouter()

router.register('submission', SubmissionViewSet, basename='submission')

urlpatterns = router.urls
