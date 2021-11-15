from django.urls import path

from .views import ScoreView, ScoreDetailView

urlpatterns = [
    path(r'', ScoreView.as_view(), name="submissions"),
    path(r'<int:id>/', ScoreDetailView.as_view(), name="submission_details"),
]
