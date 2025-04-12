from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task, TaskComment, TaskAttachment
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

User = get_user_model()

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    users = User.objects.exclude(id=request.user.id)

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'users': users
    })

@login_required
def add_task(request):
    users = User.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_id = request.POST['assigned_to']
        status = request.POST['status']
        deadline = request.POST.get('deadline')

        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to_id=assigned_to_id,
            status=status,
            deadline=deadline
        )

        if request.POST.get('text'):
            TaskComment.objects.create(
                task=task,
                user=request.user,
                content=request.POST['text']
            )

        if request.FILES.get('file'):
            TaskAttachment.objects.create(
                task=task,
                file=request.FILES['file']
            )

        return redirect('task_detail', task.id)

    return render(request, 'tasks/add_task.html', {'users': users})

@login_required
def task_list(request):
    user = request.user
    assigned_tasks = Task.objects.filter(assigned_to=user)

    todo_tasks = assigned_tasks.filter(status='todo')
    in_progress_tasks = assigned_tasks.filter(status='in_progress')
    done_tasks = assigned_tasks.filter(status='done')

    created_tasks = Task.objects.filter(assigned_by=user)

    tasks = assigned_tasks | created_tasks

    return render(request, 'tasks/task_list.html', {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'created_tasks': created_tasks
    })

@login_required
def update_task_status(request, task_id, new_status):
    task = get_object_or_404(Task, id=task_id)

    if task.assigned_to != request.user and task.assigned_by != request.user:
        return HttpResponseForbidden("Bu görevi güncelleme yetkiniz yok.")

    if new_status not in ['todo', 'in_progress', 'done']:
        return HttpResponseForbidden("Geçersiz durum.")

    task.status = new_status
    task.save()

    return redirect('task_list')

@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        content = request.POST.get("text")
        tagged_users_ids = request.POST.getlist("tagged_users")
        tagged_users = User.objects.filter(id__in=tagged_users_ids)

        comment = TaskComment.objects.create(
            task=task,
            user=request.user,
            content=content
        )

        comment.tagged_users.set(tagged_users) 
        comment.save()

        messages.success(request, "Yorum başarıyla eklendi!")
    return redirect('task_detail',  task_id=task.id)

@login_required
def add_attachment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        TaskAttachment.objects.create(task=task, file=file)
        messages.success(request, "Dosya başarıyla eklendi!")
    return redirect('task_detail', task_id=task.id)

