from django.urls import path

from .views import ProjectOrganizationView, ProjectOrganizationDetailView, QuestionExpertView, QuestionExpertDetailView

urlpatterns = [
    path('project_org/', ProjectOrganizationView.as_view(), name="project_org"),
    path('project_org/projects/<int:project>/organizations/<int:org>/', ProjectOrganizationDetailView.as_view(),
         name="project_org_details"),
    path('question_expert/', QuestionExpertView.as_view(), name="question_expert"),
    path('question_expert/questions/<int:question>/experts/<int:expert>/', QuestionExpertDetailView.as_view(),
         name="project_org_details"),
]
