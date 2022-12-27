import pandas as pd
from rest_framework import status
from rest_framework.response import Response

from project_summarizer.config.core.constants.db_constants import ProjectStatusChoice, HumanitarianChoice, \
    BudgetTypeChoice
from project_summarizer.projects.models import Sector, Address, Donor, ExecutingAgency, ImplementingPartner, \
    CounterPartMinistry, Project


def get_project_status(row_status):
    if row_status in ProjectStatusChoice.values:
        return row_status
    return None


def process_uploaded_file(file):
    name, extension = file.name.rsplit('.', maxsplit=1)
    if extension.lower() not in ['xlsx', ]:
        return Response("Unsupported File Format", status=status.HTTP_400_BAD_REQUEST)

    def dump_to_database():
        df = pd.read_excel(file)
        for idx, row in df.iterrows():
            sector, created = Sector.objects.get_or_create(
                code=row['Sector Code'],
                name=row['Sector']
            )
            address, created = Address.objects.get_or_create(
                province=row['Province'],
                district=row['District'],
                municipality=row['Municipality']
            )
            donor, created = Donor.objects.get_or_create(
                name=row['Donor']
            )
            executing_agent, created = ExecutingAgency.objects.get_or_create(
                name=row['Executing Agency']
            )
            implementing_partner, created = ImplementingPartner.objects.get_or_create(
                name=row['Implementing Partner']
            )
            counterpart_ministry, created = CounterPartMinistry.objects.get_or_create(
                name=row['Counterpart Ministry']
            )
            Project.objects.create(
                title=row['Project Title'],
                status=get_project_status(row['Project Status']),
                project_location=address,
                donor=donor,
                executing_agency=executing_agent,
                counterpart_ministry=counterpart_ministry,
                implementing_partner=implementing_partner,
                sector=sector,
                assistance_code_type=row['Type of Assistance Code'],
                budget_type=(lambda x: x if x in BudgetTypeChoice.values else None)(row['Budget Type']),
                humanitarian=(lambda x: x if x in HumanitarianChoice.values else None)(row['Humanitarian']),
                commitments=row['Commitments'],
                agreement_date=row['Agreement Date'],
                date_of_effectiveness=row['Date of Effectiveness']
            )

    dump_to_database()
    return Response('File upload success', status=status.HTTP_200_OK)
