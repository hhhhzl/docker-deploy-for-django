"""DESP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="DESP-API",
        default_version="api",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_patterns = [
    path("admin/", include("rest_framework.urls")),
    path("organizations/", include("platform_apps.organizations.urls")),
    path("users/", include("platform_apps.users.urls")),
    path("projects/", include("platform_apps.projects.urls")),
    path("questionnaires/", include("platform_apps.questionnaires.urls")),
    path("questions/", include("platform_apps.questions.urls")),
    path("submissions/", include("platform_apps.submissions.urls")),
    path("scores/", include("platform_apps.scores.urls")),
    path("junctions/", include("platform_apps.junctions.urls")),
]

docs_patterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-doc-swagger",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="api-doc-redoc",
    ),
    path(
        "swagger.yaml",
        schema_view.without_ui(cache_timeout=0),
        name="api-doc-yaml",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns)),
    path("docs/", include(docs_patterns)),
]
