from django.urls import path

from .views import SubmissionView, SubmissionDetailView

urlpatterns = [
    path(r'', SubmissionView.as_view(), name="submissions"),
    path(r'<int:id>/', SubmissionDetailView.as_view(), name="submission_details"),
]
