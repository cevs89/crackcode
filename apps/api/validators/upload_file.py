import os

import pandas
from django.utils.datastructures import MultiValueDictKeyError


def validate_header_missing(expected_headers, headers):
    missing_headers = [
        col
        for col in expected_headers
        if col.upper() not in (col.upper() for col in headers)
    ]
    if len(missing_headers) > 0:
        return missing_headers
    else:
        return True


def validate_header_garbage(expected_headers, headers):
    garbage_headers = [
        col
        for col in headers
        if col.upper() not in (col.upper() for col in expected_headers)
    ]
    if len(garbage_headers) > 0:
        return garbage_headers
    else:
        return True


class ValidateUploadFile:
    """
    El separador lo define el usuario al enviar el archivo, se valida el separador
    de su archivo lo incluye y sube el archivo, y todos los procesos se hacen con
    esa variable, incluso se podría definir separadores permitidos en la DB
    """

    def file(self, data):
        if "file_upload" in data:
            get_file = data["file_upload"]

            try:
                get_file
            except MultiValueDictKeyError:
                raise ValueError("Hay errores en el archivo, porfavor verifique")

            _ext = os.path.splitext(str(get_file))[1][1:].lower()
            if not _ext == "xlsx":
                raise ValueError("El archivo debe ser un .xlsx")

            df = pandas.read_excel(get_file.file)
            headers = list(df.head().columns)

            """
            La data del Header puede y debe ser dinamica, definiendo formatos y tipos de datos
            en la DB, asi pueden ser administrados en cualquier momento.
            """

            header_valid = [
                "student_name",
                "student_last_name",
                "student_email",
                "guardian_name",
                "guardian_last_name",
                "guardian_email",
                "guardian_document",  # Optional
                "guardian_document_type",  # Optional
                "guardian_type",  # Optional
                "salon_id",
            ]

            header_missing = validate_header_missing(header_valid, headers)
            header_garbage = validate_header_garbage(header_valid, headers)

            if header_missing is True and header_garbage is True:
                # return True
                return str(df.to_csv(header=True, index=False))

            else:
                raise ValueError(
                    "titulo de pagina invalido, solo se aceptan los siguientes valores: {}".format(
                        ",".join(header_valid)
                    )
                )

        else:
            raise ValueError(
                "Debe enviar el archivo .xlsx dentro del campo: file_upload"
            )
