from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    We extend Django's built-in AbstractUser.
    AbstractUser already gives us: username, email, password,
    first_name, last_name, is_active, is_staff, date_joined.
    We just ADD a role field and a profile_pic field on top.
    """
    ROLE_CHOICES = (
        ('seeker',   'Job Seeker'),
        ('employer', 'Employer'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='seeker'
    )
    profile_pic = models.ImageField(
        upload_to='profiles/',   # saved inside media/profiles/
        null=True,
        blank=True
    )

    # Helper methods — use these in views and templates
    def is_employer(self):
        return self.role == 'employer'

    def is_seeker(self):
        return self.role == 'seeker'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"