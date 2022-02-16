from django.shortcuts import render
from backend.models import *

def statistics_home(request):

    providers_options_dict = get_providers_names()

    context = {
        'providers_options': providers_options_dict
    }
    return render(request, 'frontend/index.html', context)


def statistics_dashboard(request, **kwargs):

    providers_options_dict = get_providers_names()

    if not kwargs['stationID'] in providers_options_dict:
        context = {'providers_options': providers_options_dict}
        return render(request, 'frontend/error.html', context)
    
    context = {
        'providers_options': providers_options_dict,
        'provider_name_var': providers_options_dict[kwargs['stationID']],
        'date_from_var': kwargs['datefrom'],
        'date_to_var': kwargs['dateto'],
    }

    return render(request, 'frontend/results.html', context)


def get_providers_names():
    return {i.providerabbr:i.providername for i in Provider.objects.all()}

