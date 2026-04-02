import json
from django.core.management.base import BaseCommand
from chat.models import CollegeInfo


class Command(BaseCommand):
    help = "Import college data from JSON file"

    def handle(self, *args, **kwargs):
        with open("college_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            CollegeInfo.objects.create(
                question=item["question"],
                answer=item["answer"]
            )

        self.stdout.write(self.style.SUCCESS("College data imported successfully!"))