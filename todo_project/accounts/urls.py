from django.urls import path
from . import views 


urlpatterns = [
    # login, logout, register
    path('login/',views.loginUser, name='login'), 
    path('register/',views.registerUser, name='register'), 
    path('logout/',views.logoutUser, name='logout'), 

    # edit username, email, password
    path('user-profile/edit/username_or_email/',views.editUserNameOrEmail, name='editUserNameOrEmail'), 
    path('user-profile/edit/password/',views.editUserPassword, name='editUserPassword'), 

    # password reset
    path('password/reset/form/', views.passwordResetForm, name='passwordResetForm'),
    path('password/reset/form/<str:uid>/<str:token>/', views.passwordResetConfirm, name='passwordResetConfirm'),
]
