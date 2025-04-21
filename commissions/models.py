from django.db import models
from django.utils.timezone import now


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]  # Ascending order

    def __str__(self):
        return self.title


class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name="comments")
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]  # Descending order

    def __str__(self):
        return f"Comment on {self.commission.title}"
