from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time',  'Full Time'),
        ('part_time',  'Part Time'),
        ('remote',     'Remote'),
        ('internship', 'Internship'),
        ('contract',   'Contract'),
    )

    title        = models.CharField(max_length=200)
    company      = models.CharField(max_length=200)
    location     = models.CharField(max_length=200)
    description  = models.TextField()
    requirements = models.TextField(blank=True)
    salary_min   = models.PositiveIntegerField(null=True, blank=True)
    salary_max   = models.PositiveIntegerField(null=True, blank=True)
    job_type     = models.CharField(
                       max_length=20,
                       choices=JOB_TYPE_CHOICES,
                       default='full_time'
                   )
    employer     = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       on_delete=models.CASCADE,
                       related_name='posted_jobs'
                   )
    is_active    = models.BooleanField(default=True)
    deadline     = models.DateField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied',     'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected',    'Rejected'),
        ('hired',       'Hired'),
    )

    job          = models.ForeignKey(
                       Job,
                       on_delete=models.CASCADE,
                       related_name='applications'
                   )
    applicant    = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       on_delete=models.CASCADE,
                       related_name='applications'
                   )
    resume      = CloudinaryField(
                    resource_type="raw",
                    folder="resumes"
                )
    cover_letter = models.TextField(blank=True)
    status       = models.CharField(
                       max_length=20,
                       choices=STATUS_CHOICES,
                       default='applied'
                   )
    applied_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"
    
class SavedJob(models.Model):
    user     = models.ForeignKey(
                   settings.AUTH_USER_MODEL,
                   on_delete=models.CASCADE,
                   related_name='saved_jobs'
               )
    job      = models.ForeignKey(
                   Job,
                   on_delete=models.CASCADE,
                   related_name='saved_by'
               )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"