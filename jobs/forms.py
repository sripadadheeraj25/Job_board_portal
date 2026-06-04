from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model  = Job
        fields = [
            'title', 'company', 'location', 'job_type',
            'description', 'requirements',
            'salary_min', 'salary_max', 'deadline',
        ]
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control'}),
            'company':      forms.TextInput(attrs={'class': 'form-control'}),
            'location':     forms.TextInput(attrs={'class': 'form-control'}),
            'job_type':     forms.Select(attrs={'class': 'form-select'}),
            'description':  forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 6
                            }),
            'requirements': forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 4
                            }),
            'salary_min':   forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max':   forms.NumberInput(attrs={'class': 'form-control'}),
            'deadline':     forms.DateInput(attrs={
                                'class': 'form-control', 'type': 'date'
                            }),
        }
        labels = {
            'salary_min': 'Minimum Salary (₹)',
            'salary_max': 'Maximum Salary (₹)',
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Why are you a good fit?'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].widget.attrs['class'] = 'form-control'