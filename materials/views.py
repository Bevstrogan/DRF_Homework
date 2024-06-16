from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.pagination import CoursePaginator, LessonPaginator
from materials.permissions import IsModerator, IsNotModerator
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
    SubscriptionSerializer,
)


class Decorate_Viewset_Methods(SwaggerAutoSchema):
    def decorate_viewset_methods(names, decorator):
        if names == "__all__":
            names = [
                "list",
                "create",
                "retrieve",
                "update",
                "partial_update",
                "destroy",
            ]

        def decorate(cls):
            for name in names:
                method = getattr(cls, name)
                setattr(cls, name, decorator(method))
            return cls

        return decorate


@Decorate_Viewset_Methods.decorate_viewset_methods(names="__all__", decorator=swagger_auto_schema(tags=['names']))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticated,
        IsModerator,
        IsNotModerator,
    ]
    pagination_class = CoursePaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]
    pagination_class = LessonPaginator


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator, IsNotModerator]


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        if Subscription.objects.filter(user=user, course=course_item).exists():
            Subscription.objects.get(user=user, course=course_item).delete()
            message = "Подписка отключена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка подключена"
        return Response({"message": message})

