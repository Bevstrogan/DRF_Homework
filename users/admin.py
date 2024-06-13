from django.contrib import admin

from users.models import User, Payment

admin.site.register(User)

@admin.register(Payment)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'payments_date', 'paid_course', 'paid_lesson', 'payment_amount', 'payment_method',)
    search_fields = ('user', 'paid_course', 'paid_lesson', 'payment_method',)


