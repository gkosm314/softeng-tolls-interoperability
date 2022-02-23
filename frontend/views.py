from django.shortcuts import render
from backend.models import *
from random import randint
from datetime import datetime
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import csv, sys
from backend.backend import update_pass_from_csv_line
from os.path import splitext, join, dirname, realpath
from os import mkdir


def statistics_home(request):
    """
    Implements /interoperability/statistics (without results)
    """

    providers_options_dict = get_providers_names()

    context = {
        'providers_options': providers_options_dict
    }
    return render(request, 'frontend/index.html', context)


def statistics_dashboard(request, **kwargs):
    """
    Implements /interoperability/statistics (with results)
    This view also passes data to the chartjs script in the template
    """

    providers_options_dict = get_providers_names()

    #Ensure that the passed parameters are okey
    if not valid_search_url(providers_options_dict, **kwargs):
        context = {'providers_options': providers_options_dict}
        return render(request, 'frontend/error.html', context)

    #Queries database and extracts data related to the station chart
    stations_labels_and_data = count_passes_per_station(kwargs['provider_Abbr'], kwargs['datefrom'], kwargs['dateto'])
    stations_labels_list = list(stations_labels_and_data.keys())    #List with all the station ids
    stations_data_list = list(stations_labels_and_data.values())    #List with the corresponding data (#passes per station)

    #Queries database and extracts data related to the pie chart
    #total_passes = #passes
    (pie_labels_and_data, total_passes) = count_passes_from_each_provider(kwargs['provider_Abbr'], kwargs['datefrom'], kwargs['dateto'])
    pie_labels_list = list(pie_labels_and_data.keys()) #List with all the provider abbrs
    pie_data_list = list(pie_labels_and_data.values()) #List with the corresponding data (#passes per provider)

    context = {
        'providers_options': providers_options_dict,
        'provider_name_var': providers_options_dict[kwargs['provider_Abbr']],
        'provider_name_abbr': kwargs['provider_Abbr'],
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
    
    return render(request, 'frontend/results.html', context)


def get_providers_names():
    """
    Returns a dictionary that contains entries of the form "AO": "attiki odos" for every provider in the database
    """

    return {i.providerabbr:i.providername for i in Provider.objects.all()}


def count_passes_per_station(my_provider_parameter, date_from, date_to):
    """
    Returns a dictionary with entries of the form "AO13": 34 (#passes per station)
    An entry exists for every provider whose tags where used to pay Passes of the provider specified by my_provider_parameter in the given period.
    """

    #qs_passes = queryset which contains all the Passes from the stations owned by provider_abbr_parameter in the given period
    my_provider_id = Provider.objects.get(providerabbr = my_provider_parameter).providerid
    qs_stations = Station.objects.filter(stationprovider = my_provider_id).all()
    qs_passes = Pass.objects.filter(stationref__stationprovider__providerid = my_provider_id, timestamp__lte = date_to, timestamp__gte = date_from)

    #Initialize each stations's counter to 0
    passes_per_station = {s.stationid:0 for s in qs_stations}

    #For each station, count each passes
    for s in qs_stations:
        passes_per_station[s.stationid] = qs_passes.filter(stationref__stationid = s.stationid).count()

    return passes_per_station


def count_passes_from_each_provider(my_provider_parameter, date_from, date_to):
    """
    Returns i) a dictionary with entries of the form "AO": 34 (#passes per provider)
    An entry exists for every station of the provider specified by my_provider_parameter in the given period.
    """

    #qs_passes = queryset which contains all the Passes from the stations owned by provider_abbr_parameter in the given period
    my_provider_id = Provider.objects.get(providerabbr = my_provider_parameter).providerid
    qs_providers = Provider.objects.all()
    qs_passes = Pass.objects.filter(stationref__stationprovider__providerid = my_provider_id, timestamp__lte = date_to, timestamp__gte = date_from)

    #Initialize each provider's counter to 0
    passes_per_provider = {prov.providerabbr:0 for prov in qs_providers}
    total_passes_counter = 0

    #For each provider, count each passes and add them to the total passes
    for p in qs_providers:
        passes_per_provider[p.providerabbr] = qs_passes.filter(vehicleref__providerabbr__providerabbr = p.providerabbr).count()
        total_passes_counter += passes_per_provider[p.providerabbr]

    #Remove providers with no passes from the dictionary that will be returned
    for k,v in passes_per_provider:
        if v == 0:
            del passes_per_provider[k]

    return (passes_per_provider,total_passes_counter)


def random_rgb_color_generator(n):
    """
    Generates N random colors, where N is a function parameter.
    Random colors are generated by producing three random numbers in the range 0-255 (red-green-blue)
    Each color is represented in by string in the format accepted by chartjs
    Returns a list of strings.
    """

    list_with_rgb_strings = []

    for i in range(n):
        random_a = str(randint(0,255))
        random_b = str(randint(0,255))
        random_c = str(randint(0,255))
        list_with_rgb_strings.append(f'rgb({random_a}, {random_b}, {random_c})')

    return list_with_rgb_strings


def valid_search_url(providers_options_dict_parameter, **kwargs):
    """
    Ensures that a url which expects to generate charts has passed valid parameters
    """

    #Check that the provider exists in the database
    if not kwargs['provider_Abbr'] in providers_options_dict_parameter:
        return False

    #Check that the dates have the expected format
    try:
        datetime.strptime(kwargs['dateto'], "%Y-%m-%d")
        datetime.strptime(kwargs['datefrom'], "%Y-%m-%d")
    except ValueError as e:
        print(e)
        return False
    else:
        return True


def handle_file(f):
    """
    Handles a file from a request.
    Receives request.FILES['file'] as a parameter. Raises an Exception if something goes wrong.
    """

    #Check that the file has a .csv extension and extract its name and extension
    (file_name, file_extension) = splitext(f.name)
    if file_extension != '.csv':
        raise Exception("Error: the file must be a .csv file")

    #Directory where the uploaded csv files are saved
    target_dir = join(dirname(realpath(__file__)), 'uploaded_files')

    #If the aforementioned directory does not exist, create it
    try:
        mkdir(target_dir)
    except FileExistsError:
        pass
    except Exception as e:
        raise e

    #Path of the new file that will be saved locally
    current_datetime_now = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    new_file_name = join(target_dir, current_datetime_now + '_' + f.name)

    #Open the file and copy the uploaded file's content inside it
    with open(new_file_name, 'wb+') as target_file:
        for chunk in f.chunks():
            target_file.write(chunk)

    #Parse the csv file and insert Passes
    with open(new_file_name) as csv_file:
        #Initialize csv reader
        csv_reader = csv.reader(csv_file, delimiter=';')

        #Skip first line(headers)
        next(csv_reader)

        #Process each line
        for row in csv_reader:
            try:
                update_pass_from_csv_line(row)
                print(row)
            except Exception as e:
                print("An unexpected error occured.")
                print("Error: {}".format(e))
                raise e


def upload_passes_view(request):
    """
    View for the page with the upload file form
    """

    if request.method == 'POST':
        #For http POST request, get the form with the submited data
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #Process the file. If something goes wrong an exception will be raised
                handle_file(request.FILES['file'])
            except Exception as e:
                #Problem occured => redirect to failures page
                print(e)
                return HttpResponseRedirect('failed_upload')
            else:
                #No problems => redirect to success page
                return HttpResponseRedirect('successful_upload')

    else:
        #For http GET request, just return the form empty
        form = UploadFileForm()   

    context = {'form_var': form}
    return render(request, 'frontend/upload.html', context)


def successful_upload_view(request): 
    """
    View for the page we get redirected to if the upload is successful
    """

    context = {}
    return render(request, 'frontend/successful_upload.html', context)      


def failed_upload_view(request): 
    """
    View for the page we get redirected to if the upload fails
    """

    context = {}
    return render(request, 'frontend/failed_upload.html', context)              