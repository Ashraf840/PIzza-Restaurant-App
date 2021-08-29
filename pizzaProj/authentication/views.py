from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .decorators import *
from django.contrib.auth.decorators import login_required


@stop_authenticated_users
def userReg(request):
    context = {
        'title': 'User Registration',
    }
    # if request.method == 'POST':
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userAuth:login')
        # If error occurs, display the form as empty again
        context['registerForm'] = form
    # Get req
    else:
        form = UserRegistrationForm()   # display empty form while tha page gets loaded
        context['registerForm'] = form
    
    return render(request, 'authentication/regForm.html', context)



@stop_authenticated_users
def userLogin(request):
    context = {
        'title': 'User Login',
    }

    # [GET req] Render the form while the page loads
    form = UserLoginForm()
    context['loginForm'] = UserLoginForm()

    # [POST req]
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Route regular users and restaurant-staffs differently
                if user.is_superuser or user.is_admin or user.is_staff:
                    return redirect('restaurantStaffApplication:home_restaurant_staffs')
                else:
                    return redirect('homeApplication:homepage')

        # Show the empty login-form again, if invalid credentials are inserted
        messages.info(request, 'Invalid Credentials!')
        # print("Invalid Credentials! %s" % ('*'*20))
        return redirect('userAuth:login')

    return render(request, 'authentication/loginForm.html', context)



@login_required(login_url='userAuth:login')
def userLogout(request):
    logout(request)
    return redirect('userAuth:login')
