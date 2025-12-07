from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("training/", views.training, name="training"),
    path("generate-cv/", views.generate_cv, name="generate_cv"),
    path("contact/", views.contact, name="contact"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("dashboard/", views.user_dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("admin/manage-users/", views.manage_users, name="manage_users"),
    path("admin/reports/", views.reports, name="reports"),
    path("admin/settings/", views.admin_settings, name="admin_settings"),
]
