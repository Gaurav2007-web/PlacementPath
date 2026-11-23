from django.contrib import admin
from .models import Task, Question, DailyLog, Project, Application, Profile

admin.site.register(Task)
admin.site.register(Question)
admin.site.register(DailyLog)
admin.site.register(Project)
admin.site.register(Application)
admin.site.register(Profile)