from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import StudentsUserProfile, UserProfile
from apps.accounts.validators import ValidateExistsUser
from apps.core.models import Countries

User = get_user_model()


class UserProfileService:
    def __init__(self, group_user: str, user_data: User, data: dict):
        self.group_user = group_user
        self.user_data = user_data
        self.data = data

    def _validate_country(self) -> Countries:
        try:
            query_country = Countries.objects.get(code__exact=self.data["country"])
        except Countries.DoesNotExist:
            raise ValueError(
                _("El pais no existe, porfavor verifique e intente de nuevo")
            )

        return query_country

    def _iter_validated_data(self, _save_models: UserProfile) -> UserProfile:
        if "document_type" in self.data:
            _save_models.document_type = self.data["document_type"]

        if "document_number" in self.data:
            _save_models.document_number = self.data["document_number"]

        if "country" in self.data:
            _save_models.country = self._validate_country()

        if self.group_user == "teacher":
            if "user_type" in self.data:
                _save_models.user_type = "PROFESOR"
        else:
            if "user_type" in self.data:
                _save_models.user_type = self.data["user_type"]

        return _save_models

    def _save_student_profile(self) -> None:
        _guardian = ValidateExistsUser(email=self.data["guardian"]).get_queryset
        if _guardian is None:
            raise ValueError(f"El guardian {self.data['guardian']} no existe")

        try:
            with transaction.atomic():
                _save_models_student = StudentsUserProfile()
                _save_models_student.user = self.user_data
                _save_models_student.guardian = _guardian
                _save_models_student.save()

        except (Exception, IntegrityError) as e:
            _msg = _("Un usuario que intenta agregar ya existe")
            if "unique" in e.args[0]:
                raise ValueError(_msg)
            else:
                raise ValueError(str(e))

    def _validate_student_profile(self) -> [bool, StudentsUserProfile]:
        try:
            _query_students = StudentsUserProfile.objects.get(user=self.user_data)
        except StudentsUserProfile.DoesNotExist:
            return False

        return _query_students

    def _update_student_profile(self, student_profile: StudentsUserProfile) -> None:
        if "guardian" in self.data:
            _guardian = ValidateExistsUser(email=self.data["guardian"]).get_queryset
            if _guardian is None:
                raise ValueError(f"El guardian {self.data['guardian']} no existe")

            try:
                with transaction.atomic():
                    student_profile.guardian = _guardian
                    student_profile.save()
            except (Exception, IntegrityError) as e:
                raise ValueError(str(e))

    def _save_user_general_profile(self) -> UserProfile:
        try:
            with transaction.atomic():
                _save_models = UserProfile()
                _save_models.user = self.user_data
                _save_models = self._iter_validated_data(_save_models)
                _save_models.save()

        except (Exception, IntegrityError) as e:
            _msg = _(
                "Un usuario con el mismo pais, tipo y numero de documento, igual al que intenta agregar ya existe"
            )
            if "unique" in e.args[0]:
                raise ValueError(_msg)
            else:
                raise ValueError(str(e))

        return _save_models

    def _validate_user_general_profile(self) -> [bool, UserProfile]:
        try:
            _query_userprofile = UserProfile.objects.get(user=self.user_data)
        except UserProfile.DoesNotExist:
            return False

        return _query_userprofile

    def _update_user_general_profile(self, _user_profile: UserProfile) -> None:
        try:
            with transaction.atomic():
                _user_profile = self._iter_validated_data(_user_profile)
                _user_profile.save()
        except (Exception, IntegrityError) as e:
            raise ValueError(str(e))

    def execute(self) -> None:
        if self.group_user == "student":
            if (_query := self._validate_student_profile()) is False:
                self._save_student_profile()
            else:
                self._update_student_profile(_query)

        if self.group_user == "teacher" or self.group_user == "guardian":
            if (_query := self._validate_user_general_profile()) is False:
                self._save_user_general_profile()
            else:
                self._update_user_general_profile(_query)
