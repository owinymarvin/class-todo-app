from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# modules for models and forms
from django.contrib.auth.models import User
from . forms import registrationForm
from django.db.models import Q

# modules for sending Email
from django.conf import settings
from django.core.mail import send_mail

# modules for password reset
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string



def registerUser(request):

    """
        Register a new user.

        Args:
            request: HttpRequest object representing the request made to the server.

        Returns:
            HttpResponse: If the user is successfully registered, redirects to the 'viewTasks' page.
                        Otherwise, renders the 'accounts/userRegistration.html' template with the registration form.

    """


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
    return render(request, 'accounts/userRegistration.html', context)




def loginUser(request):

    """
        Log in an existing user.

        Args:
            request: HttpRequest object representing the request made to the server.

        Returns:
            HttpResponse: If the user is successfully logged in, redirects to the 'viewTasks' page.
                        Otherwise, renders the 'accounts/userLogin.html' template with the login form.

    """


    page = 'login'
    if request.user.is_authenticated:
        return redirect('viewTasks')

    if request.method == 'POST':
        # pick our data from HTML
        username_or_email = request.POST['username_or_email'].lower()
        password = request.POST['password1']

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
    return render(request, 'accounts/userLogin.html', context)



def logoutUser(request):

    """
        Log out the currently authenticated user.

        Args:
            request: HttpRequest object representing the request made to the server.

        Returns:
            HttpResponse: Redirects to the 'login' page.

    """


    logout(request)
    return redirect('login')




@login_required(login_url='login')
def editUserNameOrEmail(request):

    """
        Edit the username or email of the currently authenticated user.

        Args:
            request: HttpRequest object representing the request made to the server.

        Returns:
            HttpResponse: If the form is successfully submitted and changes are saved, redirects to the 'editUserNameOrEmail' page.
                        Otherwise, renders the 'accounts/editUserNameOrEmail.html' template with the user's profile.

    """


    page = 'editUserNameOrEmail'

    userProfile = request.user

    if request.method == 'POST':
        change_username = request.POST['change_username']
        change_email = request.POST['change_email']
        user_password = request.POST['password']

        # Check if the correct user password has been entered
        correctUserPassword = authenticate(request, username=userProfile.username, password=user_password)

        if correctUserPassword:
            
            # user entered a new username
            if change_username:

                username_already_exists = User.objects.filter(username=change_username)

                if not username_already_exists:
                    old_username = request.user.username
                    userProfile.username = change_username
                    messages.success(request, f'Username changed from "{old_username}" to "{change_username}"')

                else:
                    messages.error(request,f'ERROR: The username "{change_username}" Already exists. Try using another')


            # user entered a new email address
            if change_email:

                email_already_exists = User.objects.filter(email=change_email)

                if not email_already_exists:
                    old_email = request.user.email
                    userProfile.email = change_email
                    messages.success(request, f'Email changed from "{old_email}" to "{change_email}"')

                else:
                    messages.error(request,f'ERROR: The email "{change_email}" Already exists. Try using another')
                    

            # save user and redirect
            userProfile.save()
            return redirect('editUserNameOrEmail')

            
        # correctUserPasword = False
        else:
            messages.error(request, 'Invalid password. Failed to update profile.')


    context = {'page': page, 'userProfile': userProfile}
    return render(request, 'accounts/editUserNameOrEmail.html', context)



@login_required(login_url='login')
def editUserPassword(request):

    """
        Edit the password of the currently authenticated user.

        Args:
            request: HttpRequest object representing the request made to the server.

        Returns:
            HttpResponse: If the form is successfully submitted and the password is updated, redirects to the 'editUserNameOrEmail' page.
                        Otherwise, renders the 'accounts/editUserPassword.html' template with the user's profile.

    """
     

    page = 'editUserPassword'

    userProfile = request.user

    if request.method == 'POST':
        old_password = request.POST['old_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if the correct user password has been entered
        user_with_password = authenticate(request, username=userProfile.username, password=old_password)

        if user_with_password:

            if password1 == password2:
                # Set the new password
                user_with_password.set_password(password1)
                user_with_password.save()

                messages.success(request, 'Password updated successfully.')

                # after changing password, user was logged out. Log him in
                login(request,user_with_password)

                return redirect('editUserNameOrEmail')
            
            else:
                messages.error(request, 'New passwords do not match.')


        else:
            messages.error(request, 'Invalid users password. Failed to update password.')

    context = {'page': page, 'userProfile': userProfile}
    return render(request, 'accounts/editUserPassword.html', context)




def passwordResetForm(request):

    """
        Render the password reset form to request a password reset.

        Args:
            request: HttpRequest object representing the request made to the server.

        Returns:
            HttpResponse: If the user is already authenticated, redirects to the 'viewTasks' page.
                          If the form is successfully submitted, sends a password reset email and redirects to the 'login' page.
                          Otherwise, renders the 'accounts/passwordResetForm.html' template.

    """


    page = 'passwordResetForm'

    if request.user.is_authenticated:
        return redirect('viewTasks')

    if request.method == 'POST':
        reset_email = request.POST['reset_email']

        user_with_email_exists = User.objects.filter(email=reset_email)

        if user_with_email_exists:
            # making reset token and url
            user = user_with_email_exists.first()
            uid = str(user.id)
            token = default_token_generator.make_token(user)
            password_reset_link = request.build_absolute_uri(f'{uid}/{token}/')

            # variables for sending emails
            subject = 'Todo App: Password Reset Requested'
            message = f'If you requested to change your password click on the link below. \n\n { password_reset_link } '

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
                messages.success(request, f'A PASSWORD RESET EMAIL HAS BEEN SENT TO "{user.email}" ')
            except:
                messages.error(request, f'Failed to send Email. Check your Internet Connection')

            return redirect('login')
        
        else:
            messages.error(request, "ERROR: No user account associated with the provided email.")

    else:
        pass # user has not yet submitted

    context = {'page':page}
    return render(request, 'accounts/passwordResetForm.html', context)




def passwordResetConfirm(request, uid, token):

    """
        Confirm and process the password reset request.

        Args:
            request: HttpRequest object representing the request made to the server.
            uid (str): User ID extracted from the password reset link.
            token (str): Token extracted from the password reset link.

        Returns:
            HttpResponse: If the user is already authenticated, redirects to the 'viewTasks' page.
                          If the password reset link is valid, renders the 'accounts/editUserPassword.html' template.
                          Otherwise, displays an error message.

    """

    
    page = 'passwordResetConfirm'

    if request.user.is_authenticated:
        return redirect('viewTasks')

    try:
        userProfile = User.objects.get(id=uid)
    except User.DoesNotExist:
        userProfile = None


    if userProfile is not None and default_token_generator.check_token(userProfile, token):
        email_reset_link_success = True

        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
           
            if password1 == password2:
                # Set the new password
                userProfile.set_password(password1)
                userProfile.save()

                messages.success(request, 'Password updated successfully.')

                # after changing password, user was logged out. Log him in
                login(request,userProfile)

                return redirect('viewTasks')
            
            else:
                messages.error(request, 'ERROR: New passwords do not match.')       

    else:
        email_reset_link_success = False
        messages.error(request, "The password reset link is invalid or has expired.")


    context = {'page': page,'email_reset_link_success':email_reset_link_success}
    return render(request, 'accounts/editUserPassword.html', context)
    # used same template to reset password as edit user password

