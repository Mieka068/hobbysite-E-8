from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Commission, JobApplication, Job, Profile
from django.db.models import Case, When, Value, IntegerField, Sum, Count, Q, F
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

        # Get all jobs and annotate accepted count
        jobs = Job.objects.filter(commission=commission).annotate(
            accepted_count=Count('applications', filter=Q(applications__status='Accepted')),
            open_slots=F('manpower_required') - Count('applications', filter=Q(applications__status='Accepted'))
        )

        user = self.request.user
        user_applied_jobs = set()

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            for job in jobs:
                if job.applications.filter(applicant=profile).exists():
                    user_applied_jobs.add(str(job.id))

            context["user_profile"] = profile
            context["is_owner"] = commission.poster == user
        else:
            user_applied_jobs = set()
            context["user_profile"] = None
            context["is_owner"] = False

        context.update({
            "jobs": jobs,
            "user_applied_jobs": user_applied_jobs,
        })

        return context
        


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    # Get Profile of the current user
    profile = request.user.profile

    # ❌ Prevent applying to own commission
    if job.commission.poster == request.user:
        messages.error(request, "You cannot apply to your own commission's job.")
        return redirect('commissions:detail', pk=job.commission.id)

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

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(JobApplication, pk=application_id)

    # Check if the current user is the poster of the commission
    if application.job.commission.poster != request.user:
        messages.error(request, "You do not have permission to accept this application.")
        return redirect('commissions:detail', pk=application.job.commission.id)

    # Accept the application
    application.status = 'Accepted'
    application.save()

    # After accepting, update job and commission statuses
    application.job.update_status()
    application.job.commission.update_status()

    messages.success(request, "Application accepted!")
    return redirect('commissions:job_applications', job_id=application.job.id)


@login_required
def reject_application(request, application_id):
    application = get_object_or_404(JobApplication, pk=application_id)

    # Only the commission owner can reject
    if application.job.commission.poster != request.user:
        messages.error(request, "You do not have permission to reject this application.")
        return redirect('commissions:detail', pk=application.job.commission.id)

    if application.status != "Pending":
        messages.warning(request, "Only pending applications can be rejected.")
    else:
        application.status = "Rejected"
        application.save()
        messages.success(request, "Application rejected.")

    return redirect('commissions:job_applications', job_id=application.job.id)


@login_required
def job_applications_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only the owner of the commission can view this
    if job.commission.poster != request.user:
        messages.error(request, "You do not have permission to reject this application.")
        return redirect('commissions:detail', pk=job.commission.id)

    applications = job.applications.all()

    return render(request, 'commissions/job_applications.html', {
        'job': job,
        'applications': applications,
    })


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
        job_formset = self.get_context_data()['job_formset']

        if form.is_valid() and job_formset.is_valid():
            form.instance.poster = self.request.user
            response = super().form_valid(form)
            job_formset.instance = self.object
            job_formset.save()

            # Only auto-update status if status is Open
            if self.object.status == 'Open':
                self.object.update_status()

            return response
        else:
            return self.form_invalid(form)


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
        job_formset = self.get_context_data()['job_formset']

        if form.is_valid() and job_formset.is_valid():
            response = super().form_valid(form)  # Save the commission
            job_formset.instance = self.object
            job_formset.save()  # Save the jobs

            self.object.update_status()

            return response
        else:
            return self.form_invalid(form)
