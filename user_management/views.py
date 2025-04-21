from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("/profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "user_management/profile_form.html", {"form": form})
