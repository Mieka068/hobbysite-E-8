from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from user_management.forms import ProfileForm
from user_management.models import Profile

# Create your views here.
# Registration View - transfer to Accounts app
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Profile when new User is created
            Profile.objects.create(user=user, display_name=user.username, email=user.email)
            login(request, user)
            return redirect('user_management:homepage')
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
            next_url = request.GET.get('next') or 'home' 
            return redirect('user_management:homepage')  # redirect to homepage
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Custom Logout View - transfer to Accounts app
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')