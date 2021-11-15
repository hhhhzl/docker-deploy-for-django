from django.urls import path

from .views import QuestionView, QuestionDetailView

urlpatterns = [
    path(r'', QuestionView.as_view(), name="questions"),
    path(r'<int:id>/', QuestionDetailView.as_view(), name="question_details"),
]
