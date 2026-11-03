from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from tasks.models import Task


@login_required
def home(request):
    today = timezone.localdate()
    next_week = today + timedelta(days=7)

    tasks = Task.objects.filter(user=request.user)

    # Indicadores
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    completed_tasks = tasks.filter(status='completed').count()

    # Percentual de conclusão
    completion_rate = 0

    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100)

    # Tarefas atrasadas
    overdue_tasks = tasks.filter(
        due_date__lt=today,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')

    # Tarefas próximas
    upcoming_tasks = tasks.filter(
        due_date__range=[today, next_week],
        status__in=['pending', 'in_progress']
    ).order_by('due_date')

    # Tarefas prioritárias
    priority_tasks = tasks.filter(
        priority='high'
    ).exclude(
        status='completed'
    ).order_by('due_date')

    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
        'overdue_tasks': overdue_tasks,
        'upcoming_tasks': upcoming_tasks,
        'priority_tasks': priority_tasks,
        'status_data': [
            pending_tasks,
            in_progress_tasks,
            completed_tasks
        ],
    }

    return render(request, 'home.html', context)
