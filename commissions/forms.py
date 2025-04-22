from django import forms
from .models import JobApplication, Commission, Job
from django.forms import inlineformset_factory

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []  # no fields needed from user, just triggers creation

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ['author', 'created_on', 'updated_on']
        widgets = {
            'status': forms.Select()
        }

JobFormSet = inlineformset_factory(
    Commission,
    Job,
    fields=['role', 'entry', 'manpower_required', 'status'],
    extra=1,
    can_delete=True
)