from rest_framework import serializers

from project_summarizer.projects.models import Project


class FileImportSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
