from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Commission, JobApplication, Job, Profile
from django.db.models import Case, When, Value, IntegerField, Sum, Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm, CommissionForm, JobFormSet
from django.contrib import messages
from django.urls import reverse_lazy
from commissions.models import JobApplication


class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/list.html"
    context_object_name = "commissions"

    def get_queryset(self):
        # Custom sort order for status
        status_order = Case(
            When(status='Open', then=Value(0)),
            When(status='Full', then=Value(1)),
            When(status='Completed', then=Value(2)),
            When(status='Discontinued', then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )

        return Commission.objects.all().order_by(status_order, '-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            # Commissions created by the user
            context["my_commissions"] = Commission.objects.filter(poster=user)

            # Replace the old applied_commissions query with this:
            applications = JobApplication.objects.filter(applicant=user.profile)
            applied_commission_ids = applications.values_list('job__commission_id', flat=True)
            context["applied_commissions"] = Commission.objects.filter(id__in=applied_commission_ids)
        
        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/detail.html"
    context_object_name = "commission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()

        # Get all jobs under this commission and annotate accepted_count
        jobs = Job.objects.filter(commission=commission).annotate(
            accepted_count=Count('applications', filter=Q(applications__status='Accepted'))
        )

        user = self.request.user
        user_applied_jobs = set()

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)

            # Collect job IDs (as strings) the user has applied to
            for job in jobs:
                if job.applications.filter(applicant=profile).exists():
                    user_applied_jobs.add(str(job.id))

            context["user_profile"] = profile
            context["is_owner"] = commission.poster == user
        else:
            # Not logged in: empty set, user hasn't applied to any jobs
            user_applied_jobs = set()
            context["user_profile"] = None
            context["is_owner"] = False

        # Aggregate manpower info
        total_required = jobs.aggregate(total=Sum('manpower_required'))['total'] or 0
        total_open = sum(
            max(job.manpower_required - job.accepted_count, 0) for job in jobs
        )

        context.update({
            "jobs": jobs,
            "user_applied_jobs": user_applied_jobs,  # set of string job IDs
            "total_manpower_required": total_required,
            "open_manpower": total_open,
        })

        return context

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    # Get Profile of the current user
    profile = request.user.profile

    # Check if already applied
    if JobApplication.objects.filter(job=job, applicant=profile).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('commissions:detail', pk=job.commission.id)

    # Check if job is full
    accepted_count = JobApplication.objects.filter(job=job, status='Accepted').count()
    if accepted_count >= job.manpower_required:
        messages.warning(request, "This job is already full.")
        return redirect('commissions:detail', pk=job.commission.id)

    # Save application
    JobApplication.objects.create(job=job, applicant=profile, status='Pending')
    messages.success(request, "You have successfully applied to the job.")
    return redirect('commissions:detail', pk=job.commission.id)


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_form.html"
    success_url = reverse_lazy("commissions:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['job_formset'] = JobFormSet(self.request.POST)
        else:
            data['job_formset'] = JobFormSet()
        return data

    def form_valid(self, form):
        form.instance.poster = self.request.user
        response = super().form_valid(form)
        job_formset = self.get_context_data()['job_formset']
        if job_formset.is_valid():
            job_formset.instance = self.object
            job_formset.save()
        else:
            return self.form_invalid(form)
        return response


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_form.html"
    success_url = reverse_lazy("commissions:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['job_formset'] = JobFormSet(self.request.POST, instance=self.object)
        else:
            data['job_formset'] = JobFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        response = super().form_valid(form)
        job_formset = self.get_context_data()['job_formset']
        if job_formset.is_valid():
            job_formset.save()

            # Check if all jobs are Full
            if all(job.status == 'Full' for job in self.object.jobs.all()):
                self.object.status = 'Full'
                self.object.save()

        else:
            return self.form_invalid(form)
        return response