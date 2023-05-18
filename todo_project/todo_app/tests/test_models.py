from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from todo_app.models import TodoAppModel

class TestTodoAppModel(TestCase):
    def test_todo_task_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        todo_task = TodoAppModel.objects.create(
            user=user,
            title='Test Task',
            description='Test Description',
            due_datetime=datetime.now(),
            completed=False
        )

        self.assertEqual(todo_task.user, user)
        self.assertEqual(todo_task.title, 'Test Task')
        self.assertEqual(todo_task.description, 'Test Description')
        self.assertIsNotNone(todo_task.due_datetime)
        self.assertFalse(todo_task.completed)
        self.assertIsNotNone(todo_task.created)
        self.assertIsNotNone(todo_task.updated)

    def test_todo_task_str_representation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        todo_task = TodoAppModel.objects.create(
            user=user,
            title='Test Task',
            description='Test Description',
            due_datetime=datetime.now(),
            completed=False
        )

        self.assertEqual(str(todo_task), 'Test Task')

    def test_todo_task_ordering(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        todo_task1 = TodoAppModel.objects.create(
            user=user,
            title='Task 1',
            description='Description 1',
            due_datetime=datetime.now(),
            completed=False
        )
        todo_task2 = TodoAppModel.objects.create(
            user=user,
            title='Task 2',
            description='Description 2',
            due_datetime=datetime.now(),
            completed=False
        )

        tasks = TodoAppModel.objects.all()
        self.assertEqual(tasks[0], todo_task1)
        self.assertEqual(tasks[1], todo_task2)
