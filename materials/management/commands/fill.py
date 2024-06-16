from django.core.management import BaseCommand
from users.models import Payment, User
from materials.models import Lesson, Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payment.objects.all().delete()
        User.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.create(
            email="bevstrogan@gmail.com", city="Saint-Petersburg", phone="+79052123434"
        )
        User.objects.create(
            email="takoyama@gmail.com", city="Osaka", phone="(03)3834-5577"
        )
        Course.objects.create(
            name="Python Development", description="Курс по разработке на языке python"
        )
        Lesson.objects.create(
            lesson_name="ООП",
            lesson_description="Урок по ООП",
            course=Course.objects.get(name="Python Development"),
        )
        Lesson.objects.create(
            lesson_name="DRF",
            lesson_description="Урок по DRF",
            course=Course.objects.get(name="Python Development"),
        )

        payment_list = [
            {
                "user": User.objects.get(email="bevstrogan@gmail.com"),
                "payments_date": "2024-06-12",
                "paid_course": Course.objects.get(name="Python Development"),
                "paid_lesson": Lesson.objects.get(lesson_name="ООП"),
                "payment_amount": "17000",
                "payment_method": "cash",
            },
            {
                "user": User.objects.get(email="takoyama@gmail.com"),
                "payments_date": "2024-01-02",
                "paid_course": Course.objects.get(name="Python Development"),
                "paid_lesson": Lesson.objects.get(lesson_name="DRF"),
                "payment_amount": "12500",
                "payment_method": "card",
            },
        ]

        payments = []

        for payment in payment_list:
            payments.append(Payment(**payment))

        Payment.objects.bulk_create(payments)
