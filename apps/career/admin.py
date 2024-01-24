from django.contrib import admin

from apps.career.models import Courses, Enrollments, GroupStudy, Salons

admin.site.register(Courses)
admin.site.register(Enrollments)
admin.site.register(GroupStudy)
admin.site.register(Salons)
