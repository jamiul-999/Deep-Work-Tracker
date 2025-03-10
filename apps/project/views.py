from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, Task, Entry
from apps.team.models import Team

@login_required
def projects(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.all()
    
    if request.method == "POST":
        title = request.POST.get("title")
        
        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            messages.info(request, "A project was added 😉")
            return redirect("project:projects")
    
    return render(request, "project/projects.html", {"team": team, "projects": projects})

@login_required
def project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    if request.method == "POST":
        title = request.POST.get("title")
        
        if title:
            task = Task.objects.create(team=team, project=project, created_by=request.user, title=title)
            messages.info(request, "The task was added")
            return redirect("project:project", project_id=project.id)
    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)
        
    return render(request, "project/project.html", {"team": team, "project": project, "tasks_todo": tasks_todo, "tasks_done": tasks_done})

@login_required
def edit_project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    
    if request.method == "POST":
        title = request.POST.get("title")
        
        if title:
            project.title = title
            project.save()
            
            messages.info(request, "The changes were saved 😀😀")
            
            return redirect("project:project", project_id=project.id)
    return render(request, "project/edit_project.html", {"team": team, "project": project})

@login_required
def task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    
    if request.method == "POST":
        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
        date_str = request.POST.get("date")
        time_str = datetime.now().strftime("%H:%M:%S")
        date = f"{date_str} {time_str}"
        #date = "%s %s" % (request.POST.get("date"), datetime.now().time())
        minutes_total = (hours * 60) + minutes 
        
        entry = Entry.objects.create(team=team, project=project, task=task, minutes=minutes_total, created_by=request.user, created_at=date)
    
    return render(request, "project/task.html", {"today": datetime.today(), "team": team, "project": project, "task": task})

@login_required
def edit_task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    
    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status")
        
        if title:
            task.title = title
            task.status = status
            task.save()
            messages.info(request, "Saved changes 👌")
            
            return redirect("project:task", project_id=project.id, task_id=task.id)
    
    return render(request, "project/edit_task.html", {"team": team, "project": project, "task": task})