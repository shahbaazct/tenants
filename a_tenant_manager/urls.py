from django.urls import path
from . import views

# Define the URL patterns for the tenants app
urlpatterns = [
    path("login/", views.TenantLoginView.as_view(), name="tenant_login"),
    path("user-list/", views.TenantUserListView.as_view(), name="user-list"),
]
