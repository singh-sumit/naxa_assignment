from django.db import models

# Create your models here.
from project_summarizer.config.core.constants.db_constants import ProjectStatusChoice, HumanitarianChoice, \
    BudgetTypeChoice


class Sector(models.Model):
    class Meta:
        db_table = 'sector'

    code = models.PositiveIntegerField(primary_key=True, editable=False, db_index=True)
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return f"Sector: {self.code} - {self.name}"


class Address(models.Model):
    class Meta:
        db_table = 'address'

    province = models.CharField(max_length=50, )
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.province} / {self.district} / {self.municipality}"


class Donor(models.Model):
    # A project can have multiple donor
    class Meta:
        db_table = 'donor'

    name = models.CharField(max_length=255, )

    def __str__(self):
        return f"Donor: {self.name}"


class ExecutingAgency(models.Model):
    class Meta:
        db_table = 'executing_agency'

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Executing Agency : {self.name}"


class ImplementingPartner(models.Model):
    class Meta:
        db_table = 'implementing_partner'

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Implementing Partner: {self.name}"


class CounterPartMinistry(models.Model):
    class Meta:
        db_table = 'counterpart_ministry'

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Counter Part Ministry: {self.name}"


class Project(models.Model):
    class Meta:
        db_table = 'project'

    title = models.CharField(max_length=255, )
    status = models.CharField(max_length=50, choices=ProjectStatusChoice.choices, default=ProjectStatusChoice.ON_GOING)
    project_location = models.ForeignKey(Address, on_delete=models.PROTECT, )

    donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True)
    executing_agency = models.ForeignKey(ExecutingAgency, on_delete=models.SET_NULL, null=True)
    implementing_partner = models.ForeignKey(ImplementingPartner, on_delete=models.SET_NULL, null=True)
    counterpart_ministry = models.ForeignKey(CounterPartMinistry, on_delete=models.SET_NULL, null=True)

    assistance_code_type = models.IntegerField()
    budget_type = models.CharField(max_length=10, choices=BudgetTypeChoice.choices, null=True)
    humanitarian = models.CharField(max_length=3, choices=HumanitarianChoice.choices, null=True)

    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)

    commitments = models.PositiveBigIntegerField()
    agreement_date = models.DateField()
    date_of_effectiveness = models.DateField()

    def __str__(self):
        return f"Project: {self.title}"
