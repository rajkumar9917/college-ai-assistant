import json
from django.core.management.base import BaseCommand
from chat.models import CollegeInfo

class Command(BaseCommand):
    help = "Import college data from JSON"

    def handle(self, *args, **kwargs):

        # old data delete
        CollegeInfo.objects.all().delete()

        with open("college_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = 0

        for item in data:
            CollegeInfo.objects.create(
                question=item["question"],
                answer=item["answer"]
            )
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} records imported successfully."
            )
        )