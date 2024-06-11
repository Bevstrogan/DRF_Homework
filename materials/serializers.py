from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "all"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "all"

class CourseDetailSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    course_lesson = SerializerMethodField()

    def get_course_lessons(self, course):
        lessons_set = Lesson.objects.filter(course=course.id)
        return [(lesson.lesson_name, lesson.lesson_description, lesson.lesson_url, lesson.owner) for lesson in
                lessons_set]

    def get_course_lesson_count(self, course):
        lesson_set = Lesson.objects.filter(course=course.id)
        return lesson_set.count()
    class Meta:
        model = Course
        fields = 'all'
