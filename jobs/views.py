from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Job, Application, SavedJob
from .forms import JobForm, ApplicationForm


def job_list(request):
    jobs = Job.objects.filter(is_active=True)

    # Search by keyword
    query = request.GET.get('q', '')
    if query:
        from django.db.models import Q
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)

    # Pagination — 5 jobs per page
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/job_list.html', {
        'jobs': page_obj,           # ← now page_obj instead of jobs
        'page_obj': page_obj,
        'query': query,
        'job_type': job_type,
        'location': location,
        'job_type_choices': Job.JOB_TYPE_CHOICES,
    })

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)

    already_applied = False
    is_saved = False

    if request.user.is_authenticated and request.user.is_seeker():
        already_applied = Application.objects.filter(
            job=job, applicant=request.user
        ).exists()
        is_saved = SavedJob.objects.filter(
            user=request.user, job=job
        ).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'is_saved': is_saved,
    })


@login_required
def job_create(request):
    if not request.user.is_employer():
        messages.error(request, "Only employers can post jobs.")
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # build object but don't save yet
            job.employer = request.user    # attach logged-in user as employer
            job.save()                     # now save to database
            messages.success(request, "Job posted successfully!")
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'editing': False,
    })


@login_required
def job_edit(request, pk):
    # get_object_or_404 with employer=request.user ensures only
    # the employer who posted it can edit it
    job = get_object_or_404(Job, pk=pk, employer=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)  # pre-fill form with existing data

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'editing': True,
    })


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('job_list')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)

    if request.user.is_employer():
        messages.error(request, "Employers cannot apply to jobs.")
        return redirect('job_detail', pk=pk)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job       = job
            app.applicant = request.user
            app.save()

            # Send email notification to employer
            from django.core.mail import send_mail
            send_mail(
                subject=f'New application for {job.title}',
                message=(
                    f'Hi {job.employer.username},\n\n'
                    f'{request.user.username} has applied for your job: {job.title}.\n\n'
                    f'Login to your dashboard to view the application.\n\n'
                    f'Job Board Team'
                ),
                from_email=None,   # uses DEFAULT_FROM_EMAIL
                recipient_list=[job.employer.email],
                fail_silently=True,  # don't crash if email fails
            )

            messages.success(request, "Application submitted! Good luck!")
            return redirect('seeker_dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})


@login_required
def employer_dashboard(request):
    if not request.user.is_employer():
        return redirect('seeker_dashboard')

    from django.db.models import Count
    my_jobs = Job.objects.filter(employer=request.user).annotate(
        app_count=Count('applications')
    )

    return render(request, 'jobs/employer_dashboard.html', {
        'my_jobs': my_jobs,
    })


@login_required
def seeker_dashboard(request):
    if not request.user.is_seeker():
        return redirect('employer_dashboard')

    my_applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job')

    return render(request, 'jobs/seeker_dashboard.html', {
        'applications': my_applications,
    })


@login_required
def job_applications(request, pk):
    # Only the employer who posted the job can see its applications
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    applications = job.applications.select_related('applicant')

    return render(request, 'jobs/job_applications.html', {
        'job': job,
        'applications': applications,
    })

@login_required
def update_application_status(request, pk):
    from django.http import JsonResponse
    app = get_object_or_404(Application, pk=pk, job__employer=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = [s[0] for s in Application.STATUS_CHOICES]
        if new_status in valid:
            app.status = new_status
            app.save()
            messages.success(request, f"Status updated to {app.get_status_display()}")
    return redirect('job_applications', pk=app.job.pk)

@login_required
def toggle_save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user.is_employer():
        messages.error(request, "Employers cannot save jobs.")
        return redirect('job_detail', pk=pk)

    saved = SavedJob.objects.filter(user=request.user, job=job).first()
    if saved:
        saved.delete()
        messages.info(request, "Job removed from saved list.")
    else:
        SavedJob.objects.create(user=request.user, job=job)
        messages.success(request, "Job saved!")

    return redirect('job_detail', pk=pk)


@login_required
def saved_jobs(request):
    if not request.user.is_seeker():
        return redirect('employer_dashboard')

    my_saved = SavedJob.objects.filter(
        user=request.user
    ).select_related('job')

    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': my_saved})

@login_required
def withdraw_application(request, pk):
    app = get_object_or_404(
        Application,
        pk=pk,
        applicant=request.user  # only the applicant can withdraw
    )

    # Only allow withdrawal if status is still 'applied'
    # Can't withdraw if already shortlisted or hired
    if app.status != 'applied':
        messages.error(request,
            f"Cannot withdraw — your application is already {app.get_status_display()}.")
        return redirect('seeker_dashboard')

    if request.method == 'POST':
        app.delete()
        messages.success(request, "Application withdrawn successfully.")
        return redirect('seeker_dashboard')

    return render(request, 'jobs/withdraw_confirm.html', {'app': app})