import serpy


class UsersSerializer(serpy.Serializer):
    id = serpy.Field()
    first_name = serpy.Field(label="Nombre", required=True)
    last_name = serpy.Field(label="Apellidos", required=True)
    email = serpy.Field()
    group_user = serpy.MethodField(label="Grupo de usuarios")
    details = serpy.MethodField(label="Detalles de usuarios")

    def _details_users(self, user_model):
        _array = {}
        if user_model.country:
            _array["country"] = user_model.country.name
            _array["country_code"] = user_model.country.code

        if user_model.document_type:
            _array["document_type"] = user_model.document_type

        if user_model.document_number:
            _array["document_number"] = user_model.document_number

        if user_model.user_type:
            _array["user_type"] = user_model.get_user_type_display()

        return _array

    def get_group_user(self, obj):
        if obj.groups.all():
            return obj.groups.all()[0].name

    def get_details(self, obj):
        if obj.groups.all():
            if (
                obj.groups.all()[0].name == "teacher"
                or obj.groups.all()[0].name == "guardian"
            ):
                return self._details_users(obj.user_user_profile_related)

            if obj.groups.all()[0].name == "student":
                _array = {
                    "guardian": self._details_users(
                        obj.user_students_user_profile_related.guardian.user_user_profile_related
                    )
                }
                return _array

        return {}
