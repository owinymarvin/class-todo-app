from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo_app.views import welcome, aboutUs, contactUs
from todo_app.views import createTask, updateTask, deleteTask, viewTasks
from todo_app.views import calendarView


class TestUrls(SimpleTestCase):
    def test_urls_welcome(self):
        url_welcome = reverse('welcome')
        self.assertEquals(resolve(url_welcome).func, welcome)
        # print(resolve(url_welcome))
    
    def test_urls_aboutUS(self):
        url_aboutUs = reverse('aboutUs')
        self.assertEquals(resolve(url_aboutUs).func, aboutUs)

    def test_urls_contactUs(self):
        url_contactUs = reverse('contactUs')
        self.assertEquals(resolve(url_contactUs).func, contactUs)

    def test_urls_viewTasks(self):
        url_viewTasks = reverse('viewTasks')
        self.assertEquals(resolve(url_viewTasks).func, viewTasks)

    def test_urls_createTask(self):
        url_createTask = reverse('createTask')
        self.assertEquals(resolve(url_createTask).func, createTask)

    def test_urls_updateTask(self):
        url_updateTask = reverse('updateTask' , args=[1])
        self.assertEquals(resolve(url_updateTask).func, updateTask)

    def test_urls_deleteTask(self):
        url_deleteTask = reverse('deleteTask',args=[2])
        self.assertEquals(resolve(url_deleteTask).func, deleteTask)

    def test_urls_calendarView(self):
        url_calendarView = reverse('calendarView')
        self.assertEquals(resolve(url_calendarView).func, calendarView)
