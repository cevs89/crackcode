import serpy
from django.contrib.auth import get_user_model

from apps.api.serializers.group_study import GroupStudySerializer
from apps.api.serializers.users import UsersSerializer
from apps.career.models import Enrollments

User = get_user_model()


class SalonsSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field(label="nombre")
    teacher = UsersSerializer(label="profesor")
    group_study = GroupStudySerializer(label="grupo")
    students = serpy.MethodField()

    def get_students(self, obj):
        queryset = Enrollments.objects.filter(salon_id=obj.id).values("student_id")
        return UsersSerializer(User.objects.filter(id__in=queryset), many=True).data
