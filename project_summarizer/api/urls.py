from django.urls import path,include

urlpatterns = [
    path('v1/', include('project_summarizer.api.v1.urls', namespace='v1'))
]