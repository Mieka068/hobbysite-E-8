from django.db import models
from django.utils.timezone import now


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

    class Meta:
        ordering = ['created_on']  # Ascending by default

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


