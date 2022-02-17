from django.shortcuts import render
from backend.models import *
from random import randint

import timeit

def statistics_home(request):

    providers_options_dict = get_providers_names()

    context = {
        'providers_options': providers_options_dict
    }
    return render(request, 'frontend/index.html', context)


def statistics_dashboard(request, **kwargs):

    start = timeit.default_timer()

    providers_options_dict = get_providers_names()

    if not kwargs['provider_Abbr'] in providers_options_dict:
        context = {'providers_options': providers_options_dict}
        return render(request, 'frontend/error.html', context)

    stations_labels_and_data = count_passes_per_station(kwargs['provider_Abbr'], kwargs['datefrom'], kwargs['dateto'])
    stations_labels_list = list(stations_labels_and_data.keys())
    stations_data_list = list(stations_labels_and_data.values())

    (pie_labels_and_data, total_passes) = count_passes_from_each_provider(kwargs['provider_Abbr'], kwargs['datefrom'], kwargs['dateto'])
    pie_labels_list = list(pie_labels_and_data.keys())
    pie_data_list = list(pie_labels_and_data.values())

    context = {
        'providers_options': providers_options_dict,
        'provider_name_var': providers_options_dict[kwargs['provider_Abbr']],
        'date_from_var': kwargs['datefrom'],
        'date_to_var': kwargs['dateto'],
        'stations_labels_list_str': stations_labels_list,
        'stations_data_list_str': stations_data_list,
        'stations_bg_colors_list_str': random_rgb_color_generator(len(stations_labels_list)),        
        'total_passes': total_passes,
        'pie_labels_list_str': pie_labels_list,
        'pie_data_list_str': pie_data_list,
        'pie_bg_colors_list_str': random_rgb_color_generator(len(pie_labels_list)),
    }

    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    
    return render(request, 'frontend/results.html', context)


def get_providers_names():
    return {i.providerabbr:i.providername for i in Provider.objects.all()}


def count_passes_per_station(my_provider_parameter, date_from, date_to):

    my_provider_id = Provider.objects.get(providerabbr = my_provider_parameter).providerid
    qs_stations = Station.objects.filter(stationprovider = my_provider_id).all()
    qs_passes = Pass.objects.filter(providerabbr = my_provider_id, timestamp__lte = date_to, timestamp__gte = date_from)

    passes_per_station = {s.stationid:0 for s in qs_stations}

    for s in qs_stations:
        passes_per_station[s.stationid] = qs_passes.filter(stationref__stationid = s.stationid).count()

    return passes_per_station


def count_passes_from_each_provider(my_provider_parameter, date_from, date_to):

    passes_per_provider = {prov.providerabbr:0 for prov in Provider.objects.all()}

    #QuerySet which contains all the Passes from the stations owned by provider_abbr_parameter
    my_provider_id = Provider.objects.get(providerabbr = my_provider_parameter).providerid
    qs_passes = Pass.objects.filter(providerabbr = my_provider_id, timestamp__lte = date_to, timestamp__gte = date_from)

    passes_per_provider[my_provider_parameter] = qs_passes.filter(ishome=1).count()

    total_passes_counter = passes_per_provider[my_provider_parameter]
    for p in qs_passes.exclude(ishome=1):
        passes_per_provider[p.vehicleref.providerabbr.providerabbr] += 1
        total_passes_counter += 1

    for k,v in passes_per_provider:
        if v == 0:
            del passes_per_provider[k]

    return (passes_per_provider,total_passes_counter)

def random_rgb_color_generator(n):

    list_with_rgb_strings = []

    for i in range(n):
        random_a = str(randint(0,255))
        random_b = str(randint(0,255))
        random_c = str(randint(0,255))
        list_with_rgb_strings.append(f'rgb({random_a}, {random_b}, {random_c})')

    return list_with_rgb_strings