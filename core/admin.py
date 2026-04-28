from django.contrib import admin
from .models import StudyRoom, Message, PomodoroSession

admin.site.register(StudyRoom)
admin.site.register(Message)
admin.site.register(PomodoroSession)