from django.db import models


class CollegeInfo(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question


class Message(models.Model):
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]