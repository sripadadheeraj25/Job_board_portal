from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/',        views.job_detail, name='job_detail'),
    path('job/post/',            views.job_create, name='job_create'),
    path('job/<int:pk>/edit/',   views.job_edit,   name='job_edit'),
    path('job/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('job/<int:pk>/apply/',  views.apply_job,  name='apply_job'),
    path('dashboard/employer/',  views.employer_dashboard, name='employer_dashboard'),
    path('dashboard/seeker/',    views.seeker_dashboard,   name='seeker_dashboard'),
    path('job/<int:pk>/applications/', views.job_applications, name='job_applications'),
    path('application/<int:pk>/status/', views.update_application_status, name='update_status'),
    path('job/<int:pk>/save/',  views.toggle_save_job, name='toggle_save'),
    path('saved/',              views.saved_jobs,       name='saved_jobs'),
]