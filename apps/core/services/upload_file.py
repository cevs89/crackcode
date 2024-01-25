import csv

from django.core.files.base import ContentFile


class UploadFileService:
    def __init__(self, df_file):
        self.df_file = df_file

    def dict(self):
        file_save = ContentFile(self.df_file.encode(), "file_save.csv")
        csv_content = file_save.read().decode()
        csv_reader = csv.DictReader(csv_content.splitlines())

        for row in csv_reader:
            yield row
