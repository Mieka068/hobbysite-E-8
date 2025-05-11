from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ProfileForm
from .models import Profile
from commissions.models import Commission, JobApplication

# Registration View - transfer to Accounts app
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Profile when new User is created
            Profile.objects.create(user=user, display_name=user.username, email=user.email)
            login(request, user)
            return redirect('user_management:homepage')  # redirect to homepage
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Custom Login View - Transfer to Accounts app
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_management:homepage')  # redirect to homepage
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Custom Logout View - transfer to Accounts app
@login_required
def logout_view(request):
    logout(request)
    return redirect('user_management:login')

# Profile Update View - Keep in Profile app
@login_required
def profile_update(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_management:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_management/profile_form.html', {'form': form})

# Homepage View - Keep in Profile app
def homepage(request):
    return render(request, 'user_management/homepage.html')

@login_required
def dashboard_view(request):
    user = request.user

    # Commissions created by this user
    commissions_created = Commission.objects.filter(poster=user)

    # Commissions joined (where this user's profile is accepted)
    accepted_apps = JobApplication.objects.filter(applicant=user.profile, status="Accepted")
    commissions_joined = Commission.objects.filter(
        jobs__applications__in=accepted_apps
    ).distinct()

    return render(request, 'user_management/dashboard.html', {
        'commissions_created': commissions_created,
        'commissions_joined': commissions_joined,
    })
