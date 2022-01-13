from datetime import datetime
from argparse import ArgumentTypeError
import pathlib
from os.path import join

def cli_admin_healthcheck(args):
    print("hello")
    

def cli_admin_resetpasses(args):
    print(args)
 

def cli_admin_resetstations(args):
    print(args)


def cli_admin_resetvehicles(args):
    print(args)


def cli_login(args):
    print(args)


def cli_passesperstation(args):
    print(args)


def cli_passesanalysis(args):
    print(args)


def cli_passescost(args):
    print(args)


def cli_chargesby(args):
    print(args)


def cli_admin_usermod(args):
    print(args)   


def cli_admin_users(args):
    print(args)    


def cli_admin_passesupd(args):
    print(args)         


def cli_admin_help():
    try:
        help_msg_file_path = join(pathlib.Path(__file__).parent.resolve(), 'admin_subcommand_help_message.txt')
        help_msg_file = open(help_msg_file_path,'r')
        help_msg = help_msg_file.read()
    except Exception as e:
        print("Could not find the help message.")
        print("Error: {}".format(e))
    else:
        print(help_msg)