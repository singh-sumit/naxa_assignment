from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from project_summarizer.api.v1.projects.views import ProjectViewSet

app_name = 'v1'

router = DefaultRouter(trailing_slash=True)
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns +=[
    path('schema', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
    path('docs', SpectacularRedocView.as_view(url_name='v1:schema'), name='redoc'),
]