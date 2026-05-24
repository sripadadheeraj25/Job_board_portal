from django.shortcuts import render


def job_list(request):
    # Temporary — just renders a placeholder page for now
    # We'll build the real job listing in Phase 2
    return render(request, 'jobs/job_list.html')