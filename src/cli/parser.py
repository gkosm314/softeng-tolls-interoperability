import argparse
from commands import * 

def valid_username_format(s):
	"""
	Checks if a string is a valid username. This function is used for type checking by the main parser.
	"""
	try:
		s.encode("iso-8859-1")
		return True
	except UnicodeDecodeError:
		invalid_username_error_msg = "\nInvalid username format. Usernames should not contain non-latin characters.\n"
		raise ArgumentTypeError(invalid_username_error_msg)

def valid_date_format(d):
	"""
	Checks if a string has the required format (YYYYMMDD). This function is used for type checking by the main parser.
	"""
	try:
		return datetime.strptime(d, "%Y%m%d")
	except ValueError:
		invalid_date_error_msg = "\nInvalid date format: Date does not follow the YYYYMMDD format.\nFor example, 2/7/1982 should be written as 19820712."
		print(invalid_date_error_msg)
		raise ArgumentTypeError(invalid_date_error_msg)

def setup_main_parser():
	"""
	Returns the main parser and the subparser of the 'admin' subcommand.
	These parser do not include the arguements that are specific to each admin action.
	These arguments are added seperately for each case in the main function.
	"""

	### Create the top-level parser ###
	cli_parser = argparse.ArgumentParser(description ='tolls interoperability command line tool')
	cli_subparsers = cli_parser.add_subparsers(required = True, dest = "subcommand_name") #the seleceted subcommand will be stored at dest
	cli_subparsers_list = []


	### Create the subparsers of the top-level parser###
	healthcheck_parser = cli_subparsers.add_parser('healthcheck', help = 'executes healthcheck command')
	resetpasses_parser = cli_subparsers.add_parser('resetpasses', help = 'executes resetpasses command')
	resetstations_parser = cli_subparsers.add_parser('resetstations', help = 'executes resetstations command')
	resetvehicles_parser = cli_subparsers.add_parser('resetvehicles', help = 'executes resetvehicles command')
	login_parser = cli_subparsers.add_parser('login', help = 'user login')
	passesperstation_parser = cli_subparsers.add_parser('passesperstation', help = 'executes passesperstation command')
	passesanalysis_parser = cli_subparsers.add_parser('passesanalysis', help = 'executes passesanalysis command')
	passescost_parser = cli_subparsers.add_parser('passescost', help = 'executes passescost command')
	chargesby_parser = cli_subparsers.add_parser('chargesby', help = 'executes chargesby command')
	admin_actions_parser = cli_subparsers.add_parser('admin', help = 'admin actions command', add_help = False)

	### Add all the subparsers to a list in order to manipulate them together when needed###
	cli_subparsers_list.append(healthcheck_parser)
	cli_subparsers_list.append(resetpasses_parser)
	cli_subparsers_list.append(resetstations_parser)
	cli_subparsers_list.append(resetvehicles_parser)
	cli_subparsers_list.append(login_parser)
	cli_subparsers_list.append(passesperstation_parser)
	cli_subparsers_list.append(passesanalysis_parser)
	cli_subparsers_list.append(passescost_parser)
	cli_subparsers_list.append(chargesby_parser)
	

	### Set default function that handles each subparser ###
	healthcheck_parser.set_defaults(func = cli_admin_healthcheck)
	resetpasses_parser.set_defaults(func = cli_admin_resetpasses)
	resetstations_parser.set_defaults(func = cli_admin_resetstations)
	resetstations_parser.set_defaults(func = cli_admin_resetvehicles)
	login_parser.set_defaults(func = cli_login)
	passesperstation_parser.set_defaults(func = cli_passesperstation)
	passesanalysis_parser.set_defaults(func = cli_passesanalysis)
	passescost_parser.set_defaults(func = cli_passescost)
	chargesby_parser.set_defaults(func = cli_chargesby)
	#We set admin_actions_parser's func in main() function


	### Add arguments to the subparsers ###

	#arguments for the login commnad
	login_parser.add_argument('--username', required =True, help = "user's username")
	login_parser.add_argument('--passw', required =True, help = "user's password")

	#arguments for the four main commands
	passesperstation_parser.add_argument('--station', required =True, help = "station id. examples")

	for subparser in [passesanalysis_parser, passescost_parser, chargesby_parser]:
		subparser.add_argument('--op1', required = True, help = "abbreviation of operator 1. examples: KO, AO, OO...")

	for subparser in [passesanalysis_parser, chargesby_parser]:
		subparser.add_argument('--op2', required = True, help = "abbreviation of operator 2. examples: KO, AO, OO...")

	for subparser in [passesperstation_parser, passesanalysis_parser, passescost_parser, chargesby_parser]:
		subparser.add_argument('--datefrom', required = True, help = "date in YYYYMMDD format. example: 12/7/1982 should be written 19820712", type = valid_date_format)
		subparser.add_argument('--dateto', required = True, help = "date in YYYYMMDD format. example: 12/7/1982 should be written 19820712", type = valid_date_format)

	#flags for the admin action commands
	#It is necessary to choose exactly one admin action to execute. We use a mutually_exclusive_group with required = True
	admin_action_flag_argument = admin_actions_parser.add_mutually_exclusive_group(required = True)
	admin_action_flag_argument.add_argument('-h', '--help', action='store_true', help="prints help message")
	admin_action_flag_argument.add_argument('--usermod', action='store_true', help="changes password of existing user or creates a new user")
	admin_action_flag_argument.add_argument('--users', action='store_true', help="prints info about a specific user")
	admin_action_flag_argument.add_argument('--passesupd', action='store_true', help="uploads new passes")

	#arguments for all the commands
	for subparser in cli_subparsers_list:
		subparser.add_argument('--format', choices = ['json', 'csv'] , required = True, help = "output format")

	return (cli_parser, admin_actions_parser)


def main():
	#Set up the main parser
	(main_parser, admin_parser) = setup_main_parser()

	#The main parser contains all the arguments except the arguments of the admin actions' subcommands.
	#We use parse_known_args to avoid raising an error if the arguments of an admin actions' subcommands are included.
	try:
		known_args = main_parser.parse_known_args()[0] #returns a two item tuple containing the populated namespace and the list of remaining argument strings
	except Exception as e:
		print("Error: {}".format(e))
		print("Use -h/--help argument to print help.")
		return 1

	#We then check if the 'admin' subcommand is the one the user wants to execute
	#If the user does want to execute an admin action, we:
	# 		-add the relevant arguments to the parser of the subcommand and set the 
	# 		-set the equivelant function that executes the chosen admin action
	if known_args.subcommand_name == 'admin':
		if known_args.usermod:
			admin_parser.add_argument('--username', required="True", type= valid_username_format)
			admin_parser.add_argument('--passw', required="True")
			admin_parser.set_defaults(func = cli_admin_usermod)
		elif known_args.users:
			admin_parser.add_argument('username', type= valid_username_format)
			admin_parser.set_defaults(func = cli_admin_users)
		elif known_args.passesupd:
			admin_parser.add_argument('--source', required="True")
			admin_parser.set_defaults(func = cli_admin_passesupd)
		elif known_args.help:
			cli_admin_help()
			return

	#Now that all the arguments are included for every case, parse the args and execute the command with args.func(args)
	try:
		args = main_parser.parse_args()
	except Exception as e:
		print("Error: {}".format(e))
		print("Use -h/--help argument to print help.")
		return 1
	else:
		#args.func(args)
		return 0


if __name__ == '__main__':
	main()