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
        fields = ('name', )

class CounterPartMinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterPartMinistry
        fields = ('name',)

class ExecutingAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutingAgency
        fields = ('name', )

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
