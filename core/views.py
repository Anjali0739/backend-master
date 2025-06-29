from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.shortcuts import get_object_or_404



@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Task.objects.create(
            user=request.user,  # auto assign logged-in user
            title=title,
            description=description
        )

        return redirect("/admin/")  # go back to admin after adding

    return render(request, "add_task.html")




@login_required
def my_tasks(request):
    completed_tasks = Task.objects.filter(user=request.user, completed=True).order_by('-created_at')
    incomplete_tasks = Task.objects.filter(user=request.user, completed=False).order_by('-created_at')

    return render(request, 'my_tasks.html', {
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks
    })



@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('my_tasks')



@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('my_tasks')



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
