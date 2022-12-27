from django.db import models


class ProjectStatusChoice(models.TextChoices):
    ON_GOING = 'On-Going'
    COMPLETED = 'Completed'


class HumanitarianChoice(models.TextChoices):
    YES = 'Yes'
    NO = 'No'


class BudgetTypeChoice(models.TextChoices):
    OFF_BUDGET = 'Off Budget'
    ON_BUDGET = 'On Budget'
