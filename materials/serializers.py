from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    validators = [LinkValidator(field="lesson_url")]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    course_lesson = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_course_lesson(self, course):
        lessons_set = Lesson.objects.filter(course=course.id)
        return [
            (lesson.lesson_name, lesson.lesson_description, lesson.lesson_url)
            for lesson in lessons_set
        ]

    def get_course_lesson_count(self, course):
        lesson_set = Lesson.objects.filter(course=course.id)
        return lesson_set.count()

    def get_subscription(self, obj):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return obj.subscription_set.filter(user=user).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "preview",
            "owner",
            "subscription",
            "course_lesson",
            "course_lesson_count",
        )


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
