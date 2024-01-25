import serpy

from apps.api.serializers.group_study import GroupStudySerializer
from apps.api.serializers.users import UsersSerializer


class SalonsSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field(label="nombre")
    teacher = UsersSerializer(label="profesor")
    group_study = GroupStudySerializer(label="grupo")
