<<<<<<< HEAD
=======
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
>>>>>>> 566bcc5 (Merged 'store' with user_management.)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ProfileForm
from .models import Profile
<<<<<<< HEAD
from commissions.models import Commission, JobApplication
from wiki.models import Article
from blog.models import Article as BlogArticle
from forum.models import Thread

# Profile Update View - Keep in Profile app
=======

def homepage(request):
    return render(request, 'user_management/homepage.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Profile when a new User is created
            Profile.objects.create(user=user, display_name=user.username, email=user.email)
            login(request, user)
            return redirect('home')  # redirect to homepage
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

>>>>>>> 566bcc5 (Merged 'store' with user_management.)
@login_required
def profile_update(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return redirect('user_management:profile')
=======
            return redirect('user_management:profile')  # ← fixed this line
>>>>>>> 566bcc5 (Merged 'store' with user_management.)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_management/profile_form.html', {'form': form})
<<<<<<< HEAD

# Homepage View - Keep in Profile app
def homepage(request):
    return render(request, 'user_management/homepage.html', {
        "active_page": "home",
    })

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

    # Wiki articles created by this user
    wiki_articles = Article.objects.filter(author=user.profile)

    # Blog articles created by this user
    blog_articles = BlogArticle.objects.filter(author=user.profile)

    #Forum threads posted by users
    user_threads = Thread.objects.filter(author=user)

    return render(request, 'user_management/dashboard.html', {
        'commissions_created': commissions_created,
        'commissions_joined': commissions_joined,
        'wiki_articles': wiki_articles,
        'blog_articles': blog_articles,
        'user_threads': user_threads,
    })
=======
>>>>>>> 566bcc5 (Merged 'store' with user_management.)
