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


class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name="comments")
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]  # Descending order

    def __str__(self):
        return f"Comment on {self.commission.title}"
