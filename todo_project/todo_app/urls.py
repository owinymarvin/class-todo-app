from django.urls import path
from . import views

urlpatterns = [
    # pages
    path('', views.welcome,name='welcome'),
    path('about-us/', views.aboutUs,name='aboutUs'),
    path('contact-us', views.contactUs,name='contactUs'),

    # tasks
    path('views-tasks/',views.viewTasks, name='viewTasks'),
    path('create-task/', views.createTask, name='createTask'),
    path('update-task/<str:pk>/', views.updateTask, name='updateTask'),
    path('delete-task/<str:pk>/', views.deleteTask, name='deleteTask'), 

    # calendar
    path('calendar-view/', views.calendarView, name='calendarView'),

]

