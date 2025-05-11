from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if self.email and self.user.email != self.email:
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name or self.user.username
