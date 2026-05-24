from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),

    # Django's built-in LoginView — we just point it to our template
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    # Django's built-in LogoutView — no template needed
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]