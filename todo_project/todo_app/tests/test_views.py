from django.test import TestCase, Client
from django.urls import reverse
from todo_app.models import TodoAppModel
from django.contrib.auth.models import User
from django.utils import timezone


class TestViews(TestCase):

    def test_views_welcome(self):
        client_welcome = Client()
        response_welcome = client_welcome.get(reverse('welcome'))

        self.assertEquals(response_welcome.status_code, 200)
        self.assertTemplateUsed(response_welcome, 'base/welcome.html')


    def test_views_aboutUs(self):
        client_aboutUs = Client()
        response_aboutUS = client_aboutUs.get(reverse('aboutUs'))

        self.assertEquals(response_aboutUS.status_code, 200)
        self.assertTemplateUsed(response_aboutUS, 'base/aboutUs.html')


    def test_views_contactUs(self):
        client_contactUs = Client()
        response_contactUs = client_contactUs.get( reverse('contactUs'))
        
        self.assertEquals(response_contactUs.status_code, 200)
        self.assertTemplateUsed(response_contactUs, 'base/contactUs.html')



    # tests for the various tasks views

    def test_views_viewTasks(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        client_viewTasks = Client()
        client_viewTasks.force_login(user)
        response_viewTasks = client_viewTasks.get(reverse('viewTasks'))

        self.assertEquals(response_viewTasks.status_code, 200)
        self.assertTemplateUsed(response_viewTasks, 'todo_app/viewTasks.html')


    def test_views_createTask(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        client_createTask = Client()
        client_createTask.force_login(user)
        response_createTask = client_createTask.get(reverse('createTask'))

        self.assertEquals(response_createTask.status_code, 200)
        self.assertTemplateUsed(response_createTask, 'todo_app/create_or_update_task.html')

    

    def test_views_deleteTask(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        todo_task = TodoAppModel.objects.create(
            user=user,
            title='Test Task',
            description='Test Description',
            due_datetime=timezone.now() + timezone.timedelta(days=1)  # Add a future due_datetime
        )
        client_deleteTask = Client()
        client_deleteTask.force_login(user)
        response_deleteTask = client_deleteTask.get(reverse('deleteTask', args=[todo_task.pk]))

        self.assertEquals(response_deleteTask.status_code, 200)
        self.assertTemplateUsed(response_deleteTask, 'todo_app/deleteTask.html')



