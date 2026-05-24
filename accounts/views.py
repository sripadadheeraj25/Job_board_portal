from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def register_view(request):
    """
    Handles both GET and POST for the registration page.

    GET  → user visits /accounts/register/ → show empty form
    POST → user submits form → validate → save → auto-login → redirect
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()          # saves to database, returns the user object
            login(request, user)        # auto-login after registration
            messages.success(request, f'Welcome, {user.username}! Account created.')

            # Send to different page based on their role
            if user.is_employer():
                return redirect('job_list')   # we'll build this in Phase 2
            else:
                return redirect('job_list')   # same for now, different later
    else:
        form = RegisterForm()   # empty form for GET request

    return render(request, 'accounts/register.html', {'form': form})