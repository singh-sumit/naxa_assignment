from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from project_summarizer.api.v1.projects.serializers import FileImportSerializer, ProjectSerializer, \
    ProjectFilterSerializer
from project_summarizer.config.core.utils.query_params import queryparams_to_Q
from project_summarizer.config.core.utils.read_write_files import process_uploaded_file
from project_summarizer.projects.models import Project


class ProjectViewSet(GenericViewSet, ListModelMixin):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        # sector_name = self.request.query_params.get('sector_name')
        # ministry_name = self.request.query_params.get('ministry')
        # project_status = self.request.query_params.get('project_status')

        filter_conditions = queryparams_to_Q(params_qs=self.request.query_params)
        print(filter_conditions, type(filter_conditions))

        if filter_conditions:
            queryset = Project.objects.filter(
                # sector__name__icontains=sector_name,
                # counterpart_ministry__name__icontains=ministry_name,
                # status__iexact=project_status,
                filter_conditions
            ).all()
            print("QS", queryset)
            return queryset
        return super().get_queryset()

    # def get_serializer(self, *args, **kwargs):
    #     if self.action == 'list':
    #         return ProjectFilterSerializer
    #     return super().get_serializer(*args, **kwargs)

    @extend_schema(request=FileImportSerializer)
    @action(detail=False, url_path='upload-project', name='Import Project', methods=['POST'])
    def upload_project_file(self, request):
        serializer = FileImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if file := request.data.get('file'):
            return process_uploaded_file(file)
        return Response('Project data import failed', status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = ProjectFilterSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='project-summary', name='Project Summary', methods=['GET'])
    def project_summary(self, request, *args, **kwargs):
        return Response('working')


