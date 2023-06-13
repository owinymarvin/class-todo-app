from django.core.mail import send_mail
from django.conf import settings
from todo_app .models import TodoAppModel
from datetime import timedelta,datetime
from django.utils import timezone


def check_if_task_due_30_min():

    """
        Checks if any tasks are due within the next 30 minutes and sends email notifications.
        uses the cron job in settings.py (runs every 2 minutes)

        Returns:
            None
    """


    todoTasks = TodoAppModel.objects.all()
    current_datetime = timezone.now()

    for task in todoTasks:

        # if task is not yet due. (due date greater than todays date)
        if task.due_datetime > current_datetime:

            task_remaining_time = task.due_datetime - current_datetime             

            # Task is due in 30 minutes
            if task_remaining_time < timedelta(minutes=30):

                # task email notification has not been sent already
                if task.email_notification_sent == False :

                    # send an email showing task is due                
                    send_email_task_due_in_30min(task, task_remaining_time ) 

                    # mark email as sent, save email field
                    task.email_notification_sent = True
                    task.save()    

                else:
                    pass #email already sent to the user


            else:
                pass # task is not yet 30 min to due datetime

        
        else:
            pass # task is overdue. Action will be considered later




def send_email_task_due_in_30min(task, timeRemaining):

    """
        Sends an email notification to the user for a task that is due in the next 30 minutes.

        Args:
            task: TodoAppModel object representing the task
            timeRemaining: Time remaining until the task is due

        Returns:
            None
    """


    # convert time to minutes. Put in email
    minutes_remaining = int(timeRemaining.total_seconds() // 60)

    subject = f'Todo App: Your task "{task.title}" is due in {minutes_remaining} minutes'
    message = f'Dear {task.user.username},\n\nThis is a reminder that your task "{task.title}" is due in {minutes_remaining} minutes.\n\nTask Details:\nTitle: {task.title}\nDescription: {task.description}\nDue Date: {task.due_datetime}\n\nBest regards,\nYour Task Management System'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [task.user.email]
    send_mail(subject, message, from_email, recipient_list)




def check_if_task_past_7_days():

    """
        Checks if any tasks are overdue for more than 7 days and deletes them. 
        An overdue task has past its due_datetime and is not marked as complete
        User gets an email notification that task has been deleted.

        Returns:
            None
    """


    todoTasks = TodoAppModel.objects.all()
    current_datetime = timezone.now()

    for task in todoTasks:

        # if task is duedatetime has passed. 
        if current_datetime > task.due_datetime:

            task_overdue_datetime = current_datetime - task.due_datetime                    

            # if task has passed by over 7 days 
            if task_overdue_datetime > timedelta(days=7):    

                # if task wasn't marked as completed
                if not task.completed:

                    send_email_task_deleted(task,task_overdue_datetime) 
                    task.delete() 

                else:
                    pass #task was completed. Don't delete. 

            else:
                pass # task is overdue by less than 7 days
          
        else:
            pass # task is overdue. Action will be considered later




def send_email_task_deleted(task, overdueTime):

    """
        Sends an email notification to the user for a task that has been deleted.
        A deleted task means it has been overdue by 7 days, and not marked as complete

        Args:
            task: TodoAppModel object representing the task
            overdueTime: Time the task has been overdue

        Returns:
            None
    """


    days_overdue = int(overdueTime.total_seconds() // (3600*24) )

    subject = f'Todo App: Your task "{task.title}" has been deleted.'
    message = f'Dear {task.user.username},\n\n Your task "{task.title}" has been deleted because its overdue by {days_overdue} days'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [task.user.email]
    send_mail(subject, message, from_email, recipient_list)
