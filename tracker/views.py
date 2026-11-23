import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Task, Question, DailyLog, Project, Application, Profile

def dashboard(request):
    profile, _ = Profile.objects.get_or_create(id=1)
    tasks = Task.objects.all().order_by('-created_at')
    questions = Question.objects.all().order_by('-date')
    logs = DailyLog.objects.all().order_by('-date')[:7]
    projects = Project.objects.all()
    applications = Application.objects.all().order_by('-applied_on')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    task_progress = round(completed_tasks / total_tasks * 100) if total_tasks else 0

    total_questions = questions.count()
    solved_questions = questions.filter(solved=True).count()
    question_progress = round(solved_questions / total_questions * 100) if total_questions else 0

    total_projects = projects.count()
    completed_projects = projects.filter(status='Completed').count()
    project_progress = round(completed_projects / total_projects * 100) if total_projects else 0

    core_tasks = Task.objects.filter(category='CORE')
    core_total = core_tasks.count()
    core_done = core_tasks.filter(completed=True).count()
    core_progress = round(core_done / core_total * 100) if core_total else 0

    extra_tasks = Task.objects.filter(category__in=['APTITUDE', 'INTERVIEW'])
    extra_total = extra_tasks.count()
    extra_done = extra_tasks.filter(completed=True).count()
    extra_progress = round(extra_done / extra_total * 100) if extra_total else 0

    study_score = min(DailyLog.objects.aggregate(total=Sum('study_hours'))['total'] or 0, 100)

    readiness = round(
        question_progress * 0.35 +
        core_progress * 0.25 +
        project_progress * 0.15 +
        study_score * 0.10 +
        extra_progress * 0.15
    )

    category_progress = {}
    for category, label in Task.CATEGORIES:
        items = Task.objects.filter(category=category)
        count = items.count()
        done = items.filter(completed=True).count()
        category_progress[label] = round(done / count * 100) if count else 0

    # Last 7 days data for Chart.js
    today = timezone.localdate()
    chart_labels = []
    chart_hours = []
    chart_dsa = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        log = DailyLog.objects.filter(date=day).first()
        chart_labels.append(day.strftime('%d %b'))
        chart_hours.append(float(log.study_hours) if log else 0)
        chart_dsa.append(int(log.dsa_solved) if log else 0)

    skills_list = [s.strip() for s in profile.skills.split(',') if s.strip()]

    context = {
        'profile': profile,
        'skills_list': skills_list,
        'tasks': tasks,
        'questions': questions,
        'logs': logs,
        'projects': projects,
        'applications': applications,
        'task_progress': task_progress,
        'question_progress': question_progress,
        'project_progress': project_progress,
        'readiness': readiness,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'solved_questions': solved_questions,
        'total_questions': total_questions,
        'total_projects': total_projects,
        'category_progress': category_progress,
        'total_hours': DailyLog.objects.aggregate(total=Sum('study_hours'))['total'] or 0,
        'chart_labels': json.dumps(chart_labels),
        'chart_hours': json.dumps(chart_hours),
        'chart_dsa': json.dumps(chart_dsa),
    }
    return render(request, 'tracker/dashboard.html', context)

@require_POST
def update_profile(request):
    profile, _ = Profile.objects.get_or_create(id=1)
    profile.name = request.POST.get('name', profile.name).strip()
    profile.headline = request.POST.get('headline', profile.headline).strip()
    profile.bio = request.POST.get('bio', profile.bio).strip()
    profile.skills = request.POST.get('skills', profile.skills).strip()
    profile.github_url = request.POST.get('github_url', profile.github_url).strip()
    profile.target_role = request.POST.get('target_role', profile.target_role).strip()
    profile.save()
    return redirect('dashboard')

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'DSA')
        if title:
            Task.objects.create(title=title, category=category)
    return redirect('dashboard')

@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')

@require_POST
def delete_task(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    return redirect('dashboard')

def add_log(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        hours = request.POST.get('study_hours', 0)
        solved = request.POST.get('dsa_solved', 0)
        notes = request.POST.get('notes', '')
        if date:
            DailyLog.objects.update_or_create(
                date=date,
                defaults={
                    'study_hours': hours,
                    'dsa_solved': solved,
                    'notes': notes
                }
            )
    return redirect('dashboard')

def add_question(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Question.objects.create(
                title=title,
                platform=request.POST.get('platform', 'LeetCode'),
                difficulty=request.POST.get('difficulty', 'Easy'),
                solved=request.POST.get('solved') == 'on'
            )
    return redirect('dashboard')

@require_POST
def toggle_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.solved = not question.solved
    question.save()
    return redirect('dashboard')

@require_POST
def delete_question(request, pk):
    get_object_or_404(Question, pk=pk).delete()
    return redirect('dashboard')

def add_project(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Project.objects.create(
                title=title,
                technology=request.POST.get('technology', ''),
                github_url=request.POST.get('github_url', ''),
                status=request.POST.get('status', 'In Progress'),
                description=request.POST.get('description', '')
            )
    return redirect('dashboard')

def add_application(request):
    if request.method == 'POST':
        company = request.POST.get('company', '').strip()
        if company:
            Application.objects.create(
                company=company,
                role=request.POST.get('role', 'SDE'),
                status=request.POST.get('status', 'Applied'),
                notes=request.POST.get('notes', '')
            )
    return redirect('dashboard')