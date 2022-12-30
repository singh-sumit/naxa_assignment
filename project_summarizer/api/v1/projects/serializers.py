from django.db.models import Sum
from rest_framework import serializers

from project_summarizer.projects.models import Project, Donor, Address, ImplementingPartner, CounterPartMinistry, \
    ExecutingAgency, Sector


class FileImportSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ('name',)


class ImplementingPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImplementingPartner
        fields = ('name',)


class CounterPartMinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterPartMinistry
        fields = ('name',)


class ExecutingAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutingAgency
        fields = ('name',)


class ProjectLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'province',
            'district',
            'municipality'
        )


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            'code', 'name'
        )


class ProjectFilterSerializer(serializers.ModelSerializer):
    donor = DonorSerializer()
    executing_agency = ExecutingAgencySerializer()
    implementing_partner = ImplementingPartnerSerializer()
    counterpart_ministry = CounterPartMinistrySerializer()
    project_location = ProjectLocationSerializer()
    sector = SectorSerializer()

    class Meta:
        model = Project
        exclude = ('id',)


class SectorWiseSummarySerializer(serializers.ModelSerializer):
    projects_count = serializers.SerializerMethodField()
    budget = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = (
            'code', 'name',
            'projects_count',
            'budget'
        )

    def get_projects_count(self, instance):
        return len(instance.project_set.all())

    def get_budget(self, instance):
        return instance.project_set.aggregate(budget=Sum('commitments')).get('budget')


class AddressWiseProjectSummary(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    budget = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = (
            'id',
            'name',
            'count',
            'budget',
        )

    def get_name(self, instance):
        return instance.municipality

    def get_count(self, instance):
        return instance.project_set.count()

    def get_budget(self, instance):
        return instance.project_set.aggregate(budget=Sum('commitments')).get('budget')
