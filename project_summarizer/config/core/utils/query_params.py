from django.db.models import Q

params_to_model_field = {'sector_name': 'sector__name__icontains', 'ministry': 'counterpart_ministry__name__icontains',
                         'project_status': 'status__iexact',
                         'agreement_date': 'agreement_date__exact',
                         'date_of_effectiveness': 'date_of_effectiveness__exact'}


def queryparams_to_Q(params_qs, *args, **kwargs):
    params = dict(params_qs)
    conditions = Q()
    for params_key, params_values in params.items():
        if params_key in params_to_model_field.keys():
            model_key = params_to_model_field[params_key]
            conditions &= Q((model_key, params_values[0]))
            for val in params_values[1:]:
                conditions |= Q((params_to_model_field[params_key], val))

    return conditions

# qsconditons = Q()
# qsconditons &= Q(sector__name__icontains=sector_name)
# qsconditons &= Q(counterpart_ministry__name__icontains=ministry_name)
# qsconditons &= Q(Q(status__iexact='On-Going') | Q(status__iexact='On-Going'))
# qsconditons
