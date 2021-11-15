from django.urls import path

from .views import ProjectView, ProjectDetailView, ProgressView, ProgressDetailView

urlpatterns = [
    path(r'', ProjectView.as_view(), name="projects"),
    path(r'<int:id>/', ProjectDetailView.as_view(), name="project_details"),
    path(r'<int:project>/progresses/', ProgressView.as_view(), name="progresses"),
    path(r'<int:project>/progresses/<int:id>/', ProgressDetailView.as_view(), name="progress_details"),
]
