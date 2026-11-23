from django.db import models
from django.utils import timezone

class Task(models.Model):
    CATEGORIES = [
        ('DSA', 'Data Structures & Algorithms'),
        ('CORE', 'Core CS'),
        ('AI', 'AI / ML'),
        ('APTITUDE', 'Aptitude'),
        ('DEVELOPMENT', 'Development'),
        ('INTERVIEW', 'Interview Preparation'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    DIFFICULTY = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=50, default='LeetCode')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY)
    solved = models.BooleanField(default=False)
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return self.title

class DailyLog(models.Model):
    date = models.DateField(default=timezone.localdate, unique=True)
    study_hours = models.FloatField(default=0)
    dsa_solved = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.date)

class Project(models.Model):
    title = models.CharField(max_length=150)
    technology = models.CharField(max_length=200)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=30, default='In Progress')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='SDE')
    status = models.CharField(max_length=50, default='Applied')
    applied_on = models.DateField(default=timezone.localdate)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.company
class Profile(models.Model):
    name = models.CharField(max_length=100, default='Gaurav Yadav')
    headline = models.CharField(max_length=200, default='B.Tech 5th Sem • CSE & AI | Aspiring SDE')
    bio = models.TextField(default='Passionate about Data Structures, Algorithms, AI/ML (YOLOv8, OpenCV), and Full-Stack Web Development.')
    skills = models.CharField(max_length=250, default='Python, Django, Next.js, React, YOLOv8, OpenCV, SQL')
    github_url = models.URLField(default='https://github.com/Gaurav2007-web')
    target_role = models.CharField(max_length=100, default='Software Development Engineer (SDE)')

    def __str__(self):
        return self.name