from django.urls import path

from .views import QuestionnaireView, QuestionnaireDetailView, IndicatorView, IndicatorDetailView

urlpatterns = [
    path(r'', QuestionnaireView.as_view(), name="questionnaires"),
    path(r'<int:id>/', QuestionnaireDetailView.as_view(), name="questionnaire_details"),
    path(r'<int:qnaire>/indicators/', IndicatorView.as_view(), name="indicators"),
    path(r'<int:qnaire>/indicators/<int:id>/', IndicatorDetailView.as_view(), name="indicator_details"),
]
