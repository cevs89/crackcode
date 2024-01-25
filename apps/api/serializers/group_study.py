from datetime import datetime

import serpy


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

    def get_start_time(self, obj):
        if obj.start_time is not None:
            return datetime.strftime(obj.created_at, "%Y-%m-%d %H:%M")

    def get_end_time(self, obj):
        if obj.end_time is not None:
            return datetime.strftime(obj.modified_at, "%Y-%m-%d %H:%M")
