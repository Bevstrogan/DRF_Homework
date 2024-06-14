from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView, SubscriptionCreateAPIView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyPIView.as_view(), name="lessons_delete"
    ),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path("subscription/create/", SubscriptionCreateAPIView.as_view(), name="subscription_create")
]

urlpatterns += router.urls
