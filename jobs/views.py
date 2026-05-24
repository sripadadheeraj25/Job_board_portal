from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application
from .forms import JobForm, ApplicationForm


def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)

    # Check if seeker already applied — to show correct button
    already_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'is_seeker'):
        if request.user.is_seeker():
            already_applied = Application.objects.filter(
                job=job, applicant=request.user
            ).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
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

    # Guard 1 — employers cannot apply
    if request.user.is_employer():
        messages.error(request, "Employers cannot apply to jobs.")
        return redirect('job_detail', pk=pk)

    # Guard 2 — already applied
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
            messages.success(request, "Application submitted! Good luck!")
            return redirect('seeker_dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {
        'form': form,
        'job': job,
    })


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