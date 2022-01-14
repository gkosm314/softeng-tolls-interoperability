from datetime import datetime
from argparse import ArgumentTypeError
from pathlib import Path
from os.path import join, isfile, abspath, splitext
import csv

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory

from backend.backend import update_pass_from_csv_line
from backend.backend import admin_hardreset, admin_healthcheck, admin_resetpasses, admin_resetstations, admin_resetvehicles, logout_view
from backend.backend import PassesPerStation, PassesAnalysis, PassesCost, ChargesBy, LoginView


#Helper functions
#These functions are called by the main functions (below)
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

#Main functions
#These functions are called by parser.py
def cli_admin_healthcheck(args):
    print(admin_healthcheck(args.format).data)
    

def cli_admin_resetpasses(args):
    print(admin_resetpasses(args.format).data)
 

def cli_admin_resetstations(args):
    print(admin_resetstations(args.format).data)


def cli_admin_resetvehicles(args):
    print(admin_resetvehicles(args.format).data)


def cli_login(args):
    pass


def cli_passesperstation(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/PassesPerStation/{args.station}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)

    response = PassesPerStation.as_view()(request, stationID = args.station, datefrom = args.datefrom, dateto = args.dateto)
    print(response.data)

def cli_passesanalysis(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/PassesAnalysis/{args.op1}/{args.op2}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)
    
    response = PassesAnalysis.as_view()(request, op1_ID = args.op1, op2_ID = args.op2, datefrom = args.datefrom, dateto = args.dateto)
    print(response.data)


def cli_passescost(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/PassesCost/{args.op1}/{args.op2}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)
    
    response = PassesCost.as_view()(request, op1_ID = args.op1, op2_ID = args.op2, datefrom = args.datefrom, dateto = args.dateto)
    print(response.data)


def cli_chargesby(args):
    factory = RequestFactory()
    request_path = f"/interoperability/api/ChargesBy/{args.op1}/{args.datefrom}/{args.dateto}"
    request = factory.get(request_path)
    
    response = ChargesBy.as_view()(request, op_ID = args.op1, datefrom = args.datefrom, dateto = args.dateto)
    print(response.data)


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
        help_msg_file_path = join(pathlib.Path(__file__).parent.resolve(), 'admin_subcommand_help_message.txt')
        help_msg_file = open(help_msg_file_path,'r')
        help_msg = help_msg_file.read()
    except Exception as e:
        print("Could not find the help message.")
        print("Error: {}".format(e))
    else:
        print(help_msg)