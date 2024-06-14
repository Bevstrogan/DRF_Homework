from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from materials.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.ru", password="123abc")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="course_test", description="description_test", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            lesson_name="lesson_test",
            lesson_description="description_test",
            course=self.course,
            lesson_url="https://course.youtube.com/",
            owner=self.user,
        )

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "lesson_name": "Lesson1",
            "lesson_description": "Description_test",
            "course": self.course.id,
            "lesson_url": "https://course1.youtube.com/",
            "owner": self.user.id,
        }
        response = self.client.post(url, data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(
            response.json(),
            {'course': 1,
                'id': 2,
                'lesson_description': 'Description_test',
                'lesson_name': 'Lesson1',
                'lesson_preview': None,
                'lesson_url': 'https://course1.youtube.com/',
                'owner': 1},
        )

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("lesson_name"), self.lesson.lesson_name)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"lesson_name": "Lesson1_update", "lesson_description": "Description_update"}
        response = self.client.patch(url, data)
        data1 = response.json
        print(data1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("lesson_name"), "Lesson1_update")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        print(f"{self.lesson.lesson_name} удалён")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

        # self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)