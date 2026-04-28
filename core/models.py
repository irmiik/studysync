from django.db import models
from django.contrib.auth.models import User

class StudyRoom(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="joined_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class PomodoroSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField()  # dakika
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    room = models.OneToOneField(StudyRoom, on_delete=models.CASCADE)
    content = models.TextField(blank=True)