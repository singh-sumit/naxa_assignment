from django.db.models import Count, Sum
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from project_summarizer.api.v1.projects.serializers import FileImportSerializer, ProjectSerializer, \
    ProjectFilterSerializer, SectorWiseSummarySerializer, AddressWiseProjectSummary
from project_summarizer.config.core.utils.query_params import queryparams_to_Q
from project_summarizer.config.core.utils.read_write_files import process_uploaded_file
from project_summarizer.projects.models import Project, Sector, Address


class ProjectViewSet(GenericViewSet, ListModelMixin):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):

        filter_conditions = queryparams_to_Q(params_qs=self.request.query_params)

        if self.action in ['list', 'project_summary'] and filter_conditions:
            queryset = Project.objects.filter(
                filter_conditions
            ).all()
            return queryset
        elif self.action in ['project_summary_by_location']:
            return Address.objects.filter(
                filter_conditions
            ).all()
        return super().get_queryset()

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

    @extend_schema(parameters=[
        OpenApiParameter(
            name='sector_name',
            description='Name of sector',
        ),
        OpenApiParameter(
            name='project_status',
            description='Status of Project',
            enum=['On-Going', 'Completed']
        ),
        OpenApiParameter(
            name='ministry',
            description='Counterpart ministry name'
        ),
        OpenApiParameter(
            name='agreement_date',
            description='Project Agreement date'
        ),
        OpenApiParameter(
            name='date_of_effectiveness',
            description='Project date of Effectiveness'
        ),
    ],
        responses={
            200: inline_serializer(
                name='Project Summary by sector',
                fields={
                    "total_budgets": serializers.IntegerField(),
                    "project_counts": serializers.IntegerField(),
                    "sectors": SectorWiseSummarySerializer(many=True)
                }
            )
        }
    )
    @action(detail=False, url_path='project-summary', name='Project Summary', methods=['GET'])
    def project_summary(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        data = queryset.aggregate(total_budgets=Sum('commitments'), project_counts=Count('id'))
        serializer = SectorWiseSummarySerializer(
            Sector.objects.filter(code__in=list(queryset.values_list('sector__code', flat=True).distinct())), many=True)
        data['sectors'] = serializer.data
        return Response(data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='municipality',
                description='Name of municipality',
            ),
            OpenApiParameter(
                name='district',
                description='Name of district',
            ),
            OpenApiParameter(
                name='province',
                description='Name of province',
            ),
        ],
        responses={
            200: AddressWiseProjectSummary
        }
    )
    @action(detail=False, url_path='summary-by-location', name='Project summary by location', methods=['GET'])
    def project_summary_by_location(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = AddressWiseProjectSummary(queryset, many=True)
        return Response(serializer.data)
