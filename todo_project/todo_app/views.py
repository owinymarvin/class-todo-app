from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import TodoAppForm
from . models import TodoAppModel
import datetime
import json


# Create your views here.
def welcome(request):
    
    if request.user.is_authenticated:
        return redirect('viewTasks')
    
    page = 'welcome'
    context = {'page':page,}
    return render(request,'base/welcome.html',context)


def aboutUs(request):
    page = 'aboutUs'
    context = {'page':page,}
    return render(request,'base/aboutUs.html',context)


def contactUs(request):
    page = 'contactUs'
    context = {'page':page,}
    return render(request,'base/contactUs.html',context)


@login_required(login_url='login')
def viewTasks(request):
    page = 'home'
    todoTask = TodoAppModel.objects.filter(user=request.user)

        # date_string = request.POST['due_date']
        # time_string = request.POST['due_time']

        # # combines date and time. Format becomes datetime
        # due_datetime = datetime.datetime.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M')
    context = {'page': page, 'todoTask': todoTask}
    return render(request, 'todo_app/viewTasks.html', context)


@login_required(login_url='login')
def createTask(request):
    page = 'createTask'
    todoTaskCreate = TodoAppForm()

    if request.method == 'POST':

        date_string = request.POST['due_date']
        time_string = request.POST['due_time']

        # combine date and time from user input
        due_datetime = datetime.datetime.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M')

        # task should be for a future date only.
        if due_datetime > datetime.datetime.now():
            todoTaskCreate = TodoAppForm(request.POST or None)

            if todoTaskCreate.is_valid():
                todo_task = todoTaskCreate.save(commit=False)

                # add user field
                todo_task.user = request.user

                # add datetime to the task 
                todo_task.due_datetime = due_datetime

                todo_task.save()
                return redirect('viewTasks')
            else:
                messages.error(request, 'ERROR: The task can\'t be created because the form is invalid')

        # task is due on a past date. we dont allow
        else:
            messages.error(request,'ERROR: Tasks can only be created for future dates')


    context = {'page': page, 'todoTaskCreate': todoTaskCreate}
    return render(request, 'todo_app/create_or_update_task.html', context)



@login_required(login_url='login')
def updateTask(request, pk):
    page = 'updateTask'

    todoTask = TodoAppModel.objects.get(id=int(pk))
    todoTaskCreate = TodoAppForm(instance=todoTask)

    if request.method == 'POST':
        todoTaskCreate = TodoAppForm(request.POST, instance=todoTask)

        if todoTaskCreate.is_valid():
            todoTaskCreate.save()
            return redirect('viewTasks')
        else:
            messages.error(
                request, 'ERROR: The task can\'t be created because the form is invalid')

    context = {'page': page, 'todoTaskCreate': todoTaskCreate}
    return render(request, 'todo_app/create_or_update_task.html', context)



@login_required(login_url='login')
def deleteTask(request, pk):
    page = 'deleteTask'

    todoTask = TodoAppModel.objects.get(id=int(pk))
    if request.method == 'POST':
        todoTask.delete()
        return redirect('viewTasks')

    context = {'page': page, 'todoTask': todoTask}
    return render(request, 'todo_app/deleteTask.html', context)



@login_required(login_url='login')
def calendarView(request):
    page = 'calendar'

    todo_app_tasks = TodoAppModel.objects.filter(user=request.user)

    # Convert tasks to JSON format for FullCalendar
    calendarEvents = []
    
    for task in todo_app_tasks:
        event = {
            'id': task.id,
            'title': task.title,
            'description':task.description,
            'start': task.due_datetime.isoformat(),
            'end': task.due_datetime.isoformat(),
        }
        calendarEvents.append(event)


    context = {'page': page, 'calendarEvents_json': json.dumps(calendarEvents)}
    return render(request, 'todo_app/calendarView.html', context)

