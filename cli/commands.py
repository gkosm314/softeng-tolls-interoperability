from datetime import datetime
from argparse import ArgumentTypeError
from pathlib import Path
from os.path import join, isfile, abspath, splitext, isdir, split
import csv

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory

from backend.backend import update_pass_from_csv_line
from backend.backend import admin_hardreset, admin_healthcheck, admin_resetpasses, admin_resetstations, admin_resetvehicles
from backend.backend import PassesPerStation, PassesAnalysis, PassesCost, ChargesBy, LoginView
from django.db import transaction
import json

#Helper functions
#These functions are called by the main functions (below)
def output_response_data(response_data, format, output_path_parameter):
    """
    Print the data returned to us by the backend.
    """

    if format == 'json':
        formatted_response = json.dumps(response_data, default=str, indent=4)
    else:  # response_data is a csv
        formatted_response = response_data

    #Check if we want to print the result at the standard output
    if output_path_parameter == "stdout":
        print(formatted_response)
    
    #Otherwise:
    else:
        #Convert parameter to absolute path, in case it is a relative path.
        output_path = abspath(output_path_parameter)
        
        #Find the extension of the filename
        dir, basename = split(output_path)

        #Check if the direcory exists.
        if not isdir(dir):
            print(f"Error: Directory {dir} does not exist.")
            return False

        if isfile(output_path):
            if input(f"Warning: File {output_path} already exists. Enter 'Y' to overwrite it.\n") != 'Y':
                return False

        with open(output_path,"w+") as f:
            print(formatted_response, file = f)

    return True


@transaction.atomic
def cli_create_user(username, password):
    """
    Create new user with the given username and set his password to be the given password
    """
    print("Creating new user {}...".format(username))

    try:
        new_user = User.objects.create_user(username, username+'@tolls.gr', password)
        new_user.save()
    except Exception as e:
        print("Could not create new user {}.".format(username))
        print("Error: {}".format(e))
    else:
        print("New user {} created.".format(username))    


def cli_change_password(user_object, username, password):
    """
    Change the password of a django User object and save it to the database
    """
    print("Changing password of user {}...".format(username))

    try:
        user_object.set_password(password) #Takes care of hashing automatically
        user_object.save()
    except Exception as e:
        print("Could not change password of user {}.".format(username))
        print("Error: {}".format(e))
    else:
        print("Changed password of user {} successfully.".format(username))


def output_extractor(response_object, format_parameter):
    if format_parameter == "json":
        return response_object.data
    else:
        return response_object.content.decode('utf-8')

#Main functions
#These functions are called by parser.py
def cli_admin_healthcheck(args):
    command_output = output_extractor(admin_healthcheck(args.format), args.format)
    return output_response_data(command_output, args.format, args.output)
    

def cli_admin_resetpasses(args):
    command_output = output_extractor(admin_resetpasses(args.format), args.format)
    return output_response_data(command_output, args.format, args.output)
 

def cli_admin_resetstations(args):
    command_output = output_extractor(admin_resetstations(args.format), args.format)
    return output_response_data(command_output, args.format, args.output)


def cli_admin_resetvehicles(args):
    command_output = output_extractor(admin_resetvehicles(args.format), args.format)
    return output_response_data(command_output, args.format, args.output)


def cli_login(args):
    factory = RequestFactory()
    request_path = "/interoperability/api/login/"
    request_data = {'username': args.username, 'password': args.passw}
    request = factory.post(request_path, request_data)

    response = LoginView.as_view()(request)
    return output_response_data(response.content, args.format, args.output)


def cli_passesperstation(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/PassesPerStation/{args.station}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)
    mycopy = request.GET.copy()
    mycopy['format'] = args.format
    request.GET = mycopy
    response = PassesPerStation.as_view()(request, stationID = args.station, datefrom = args.datefrom, dateto = args.dateto)
    command_output = output_extractor(response, args.format)
    return output_response_data(command_output, args.format, args.output)


def cli_passesanalysis(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/PassesAnalysis/{args.op1}/{args.op2}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)

    mycopy = request.GET.copy()
    mycopy['format'] = args.format
    request.GET = mycopy
    # response = PassesAnalysis.as_view()(request, op1_ID = args.op1, op2_ID = args.op2, datefrom = args.datefrom, dateto = args.dateto, *myargs,**kwargs)
    response = PassesAnalysis.as_view()(request, op1_ID = args.op1, op2_ID = args.op2, datefrom = args.datefrom, dateto = args.dateto)
    # print(f"response: {response}")
    command_output = output_extractor(response, args.format)
    return output_response_data(command_output, args.format, args.output)


def cli_passescost(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/PassesCost/{args.op1}/{args.op2}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)
    mycopy = request.GET.copy()
    mycopy['format'] = args.format
    request.GET = mycopy
    response = PassesCost.as_view()(request, op1_ID = args.op1, op2_ID = args.op2, datefrom = args.datefrom, dateto = args.dateto)
    command_output = output_extractor(response, args.format)
    return output_response_data(command_output, args.format, args.output)


def cli_chargesby(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/ChargesBy/{args.op1}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)
    mycopy = request.GET.copy()
    mycopy['format'] = args.format
    request.GET = mycopy
    response = ChargesBy.as_view()(request, op_ID = args.op1, datefrom = args.datefrom, dateto = args.dateto)
    command_output = output_extractor(response, args.format)
    return output_response_data(command_output, args.format, args.output)


def cli_admin_usermod(args):
    """
    If no user exists with such username, create a new one and set his password
    If a user is found, change his password
    """
    print("Searching for user {}...".format(args.username))

    #Search for user with the given username
    try:
        u = User.objects.get(username = args.username) #Raises DoesNotExist if no user found
    except ObjectDoesNotExist as e:
        print("User {} does not exist.".format(args.username))
        cli_create_user(args.username, args.passw)
    except Exception as e:
        print("An unexpected error occured.")
        print("Error: {}".format(e))
    else:
        cli_change_password(u, args.username, args.passw)


def cli_admin_users(args):
    """
    Prints information about a specific user
    """
    print("Searching for user {}...".format(args.username))

    #Search for user with the given username
    try:
        u = User.objects.get(username = args.username)
    except ObjectDoesNotExist as e:
        print("User {} does not exist.".format(args.username))
    except Exception as e:
        print("An unexpected error occured.")
        print("Error: {}".format(e))
    else:
        group_string = "".join([str(g) for g in u.groups.all()])
        print("User {} found.".format(args.username))
        print("----------------------------------------------------")
        print("User: {}\nEmail: {}\nGroups: {}\nIs superuser: {}\nDate joined: {}".format(u.username,u.email,group_string,u.is_superuser,u.date_joined))
        print("----------------------------------------------------")


def cli_admin_passesupd(args):
    """
    Inserts Passes from a csv file. The csv file is given as a parameter inside args.
    """
    
    #Check if the given path corresponds to a file
    csv_file_path = abspath(args.source)
    if not isfile(csv_file_path):
        print("Error: could not find csv file at path {}".format(csv_file_path))
        return 1

    #Check that the file has a .csv extension
    if splitext(args.source)[1] != '.csv':
        print("Error: the file must be a .csv file")
        return 1        

    with open(csv_file_path) as csv_file:
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


def cli_admin_help():
    """
    Prints help message for 'admin' subcommand from a txt file.
    """

    try:
        help_msg_file_path = join(Path(__file__).parent.resolve(), 'admin_subcommand_help_message.txt')
        help_msg_file = open(help_msg_file_path,'r')
        help_msg = help_msg_file.read()
    except Exception as e:
        print("Could not find the help message.")
        print("Error: {}".format(e))
    else:
        print(help_msg)