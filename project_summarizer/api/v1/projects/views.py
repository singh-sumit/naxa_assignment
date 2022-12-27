from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from project_summarizer.api.v1.projects.serializers import FileImportSerializer, ProjectSerializer
from project_summarizer.config.core.utils.read_write_files import process_uploaded_file


class ProjectViewSet(GenericViewSet):
    serializer_class = ProjectSerializer

    @extend_schema(request=FileImportSerializer)
    @action(detail=False, url_path='upload-project', name='Import Project', methods=['POST'])
    def upload_project_file(self, request):
        serializer = FileImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if file := request.data.get('file'):
            return process_uploaded_file(file)
        return Response('Project data import failed', status=status.HTTP_400_BAD_REQUEST)
