from django.urls import path

from .views import OrganizationView, OrganizationDetailView

urlpatterns = [
    path(r'', OrganizationView.as_view(), name="organizations"),
    path(r'<int:id>/', OrganizationDetailView.as_view(), name="organization_details")
]
