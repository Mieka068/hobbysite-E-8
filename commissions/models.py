from django.db import models
from django.utils.timezone import now
from user_management.models import Profile
from django.contrib.auth.models import User


class Commission(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commissions')

    class Meta:
        ordering = ['created_on']  # Ascending by default

    def update_status(self):
        # Only set to Full if ALL jobs are Full
        jobs = self.jobs.all()

        if all(job.status == 'Full' for job in self.jobs.all()):
            if self.status != 'Full':
                self.status = 'Full'
                self.save()
        else:
            if self.status != 'Open':
                self.status = 'Open'
                self.save()

    def __str__(self):
        return f"{self.title} ({self.status})"


class Job(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name="jobs")
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    
    def update_status(self):
        accepted_count = self.applications.filter(status='Accepted').count()
        if accepted_count >= self.manpower_required:
            if self.status != 'Full':
                self.status = 'Full'
                self.save()
        else:
            if self.status != 'Open':
                self.status = 'Open'
                self.save()


    def __str__(self):
        return f"{self.role} ({self.status})"

    class Meta:
        # Custom ordering: Open < Full, so we use a CASE WHEN to simulate it
        ordering = [
            models.Case(
                models.When(status='Open', then=models.Value(0)),
                models.When(status='Full', then=models.Value(1)),
                output_field=models.IntegerField(),
            ),
            '-manpower_required',
            'role',
        ]


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="job_applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.display_name} - {self.job.role} ({self.status})"

    class Meta:
        ordering = [
            models.Case(
                models.When(status='Pending', then=models.Value(0)),
                models.When(status='Accepted', then=models.Value(1)),
                models.When(status='Rejected', then=models.Value(2)),
                output_field=models.IntegerField(),
            ),
            '-applied_on',
        ]
