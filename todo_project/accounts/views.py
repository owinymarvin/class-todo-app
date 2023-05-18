from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . forms import registrationForm, UserProfileForm
from . models import UserProfile
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q



def registerUser(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('viewTasks')

    registration = registrationForm()

    if request.method == 'POST':
        # data is filled into the form
        registrationData = registrationForm(request.POST)

        if registrationData.is_valid():
            new_user = registrationData.save(commit=False)
            new_user.username = new_user.username.lower()

            # save the user
            new_user.save()
            login(request, new_user)


            # sending an email
            subject = 'Todo App: Thank you for Registering'
            message = f'Hi {new_user.username}, thanks for signing up, hope you will enjoy using this app.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [new_user.email]
            send_mail(subject, message, from_email,recipient_list, fail_silently=True)

            # redirect them to the home/viewtasks page if successful
            return redirect('viewTasks')
        
        else:
            messages.error(
                request, 'ERROR:  The user form was not valid. Failed to create new user')
            
    else:
        # messages.error(request,'ERROR:  Submit form using mmethod \"POST\"')
        pass

    context = {'page': page,'registrationForm': registration }
    return render(request, 'accounts/register.html', context)



def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('viewTasks')

    if request.method == 'POST':
        # pick our data from HTML
        username_or_email = request.POST['username_or_email'].lower()
        password = request.POST.get('password')

        try:
            # try to get users username and email from database
            user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email))

            # authenticates user if correct user password is applied to username or email, returns db_user
            db_user = authenticate(
                request, username=user.username, password=password)
            

            if db_user is not None:
                login(request, db_user)

                # sending an email when user logs in
                subject = 'Todo App: Someone logged into your account'
                message = f'Hi {request.user.username}, \n You have successfully logged into your account.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]
                send_mail(subject, message, from_email,recipient_list, fail_silently=True)

                # redirect user viewTasks.
                return redirect ( 'viewTasks' )
            else:
                messages.error(
                    request, "ERROR: invalid username or password, please check the login details and try again.")

        except User.DoesNotExist:
            messages.error(
                request, "ERROR: invalid login credentials, please try agin.")

    context = {'page': page}
    return render(request, 'accounts/login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')



# Users Profile
def userProfile(request):
    page = 'userProfile'

    try:
        # Create a UserProfile instance for the new user, if it already exists, skipps
        UserProfile.objects.create(user=request.user)
    except:
        pass


    user_profile = UserProfile.objects.get(user=request.user)
    user_profile_form = UserProfileForm()

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('userProfile')
    else:
        user_profile_form = UserProfileForm(instance=user_profile)

    context = {'page':page,'userProfile': user_profile_form}
    return render(request, 'accounts/userProfile.html', context)


