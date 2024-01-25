from datetime import datetime

import serpy
from django.contrib.auth import get_user_model

from apps.api.serializers.users import UsersSerializer
from apps.career.models import Enrollments

User = get_user_model()


class CoursesSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()
    description = serpy.Field()


class GroupStudySerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field(label="Nombre", required=True)
    description = serpy.Field(label="Descripción")
    course = CoursesSerializer()
    start_time = serpy.MethodField()
    end_time = serpy.MethodField()
    students = serpy.MethodField()

    def get_start_time(self, obj):
        if obj.start_time is not None:
            return datetime.strftime(obj.created_at, "%Y-%m-%d %H:%M")

    def get_end_time(self, obj):
        if obj.end_time is not None:
            return datetime.strftime(obj.modified_at, "%Y-%m-%d %H:%M")

    def get_students(self, obj):
        queryset = Enrollments.objects.filter(group_study=obj.id).values("student_id")
        return UsersSerializer(User.objects.filter(id__in=queryset), many=True).data
