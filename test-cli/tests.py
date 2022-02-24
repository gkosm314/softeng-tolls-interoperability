import os.path

from django.test import TestCase
from cli.commands import *
from contextlib import redirect_stdout
import io
from argparse import Namespace
from rest_framework.response import Response
from django.http import HttpResponse
from cli.parser import *
import cli.commands
# Create your tests here.


class TestOutputResponseData(TestCase):
    """
    Test the functionality of the output_response_data function
    output_response_data(response_data, format, output_path_parameter):
    Test Data:
     - test-cli/test_data/csv_response_data.txt
     - test-cli/test_data/json_response_data.json
    """
    def setUp(self) -> None:
        """
        Loads the appropriate data on the corresponding variables
        These files are created by the backend functions and contain the raw data that are used to generate Response
        objects
        """
        self.csv_path = 'test-cli/test_data/csv_response_data.txt'
        self.json_path = 'test-cli/test_data/json_response_data.json'
        with open(self.json_path, 'r') as f:
            self.json_response = json.load(f)
        with open(self.csv_path, 'r') as f:
            self.csv_response = f.read()
            # Remove trailing new lines
            self.csv_response = self.csv_response.rstrip()
        self.json_output_file = 'test-cli/test_data/json_output.json'
        self.csv_output_file = 'test-cli/test_data/csv_output.txt'

    def test_output_stdout_json(self):
        """
        Test that the json output is correctly printed in the stdout
        """
        f = io.StringIO()
        with redirect_stdout(f):
            output_response_data(self.json_response, format='json', output_path_parameter='stdout')
        s = f.getvalue()
        self.assertJSONEqual(json.dumps(self.json_response), s)

    def test_output_stdout_csv(self):
        """
        Test that the csv output is correctly printed in the stdout
        """
        f = io.StringIO()
        with redirect_stdout(f):
            output_response_data(self.csv_response, format='csv', output_path_parameter='stdout')
        s = f.getvalue()
        # Remove trailing new lines for output
        s = s.rstrip()
        self.assertEqual(self.csv_response, s)

    def test_output_file_json(self):
        """
         Test that the output is correctly dumped in a json file
         """
        output_response_data(self.json_response, format='json', output_path_parameter=self.json_output_file)
        self.assertTrue(os.path.isfile(self.json_output_file))
        with open(self.json_output_file, 'r') as f:
            file_content = json.load(f)
        self.assertJSONEqual(json.dumps(file_content), self.json_response)

    def test_output_file_csv(self):
        """
         Test that the output is correctly dumped in a csv file
         """
        output_response_data(self.csv_response, format='csv', output_path_parameter=self.csv_output_file)
        self.assertTrue(os.path.isfile(self.csv_output_file))
        with open(self.csv_output_file, 'r') as f:
            file_content = f.read()
            file_content = file_content.rstrip()
        self.assertEqual(self.csv_response, file_content)


    def tearDown(self):
        """
        Delete the file if it exists so future runs are not impacted
        """
        if os.path.isfile(self.json_output_file):
            os.remove(self.json_output_file)
        if os.path.isfile(self.csv_output_file):
            os.remove(self.csv_output_file)


class TestCliCreateUser(TestCase):
    """
    Tests the cli_create_user function
    cli_create_user(username, password)
    """

    def setUp(self) -> None:
        self.username = 'CliTestUsername'
        self.password = 'CliTestUsernamePassword123'
        # Make sure the user doesn't exist already
        self.assertFalse(User.objects.filter(username=self.username).exists())
        # Make sure the user exists
        cli_create_user(self.username, self.password)
        self.user = User.objects.get(username=self.username)
        # Error message should be on test-cli/test_data/create_user_error.txt file
        with open('test-cli/test_data/create_user_error.txt', 'r') as f:
            self.error_msg = f.read()

    def test_user_is_created(self):
        """
        Tests that the function can indeed create a user
        """
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_password_is_correct(self):
        """
        Tests that the password is correct
        """
        self.assertTrue(self.user.check_password(self.password))

    def test_user_already_exists(self):
        """
        If we try to create the same user we should get an exception
        The exception is handled by the function but we can get notified by the message
        """
        f = io.StringIO()
        with redirect_stdout(f):
            cli_create_user(self.username, self.password)
        s = f.getvalue()
        self.assertEqual(s, self.error_msg)

    def tearDown(self) -> None:
        """
        Removes the user so other tests aren't impacted
        """
        self.user.delete()


class TestCliChangePassword(TestCase):
    """
    Test the cli_change_password function
    cli_change_password(user_object, username, password)
    """

    def setUp(self) -> None:
        """
        Creates a user to be used for each TC
        """
        self.username = 'CliTestUsername'
        self.password = 'CliTestUsernamePassword123'
        self.new_password = 'NEW_CliTestUsernamePassword123'
        self.email = 'CliTestUsername@email.com'
        self.user = User.objects.create_user(username=self.username,
                                             email=self.email,
                                             password=self.password)

    def tearDown(self) -> None:
        """
        Deletes the user created on setup so it doesn't affect other TCs
        """
        self.user.delete()

    def test_old_password_not_working(self):
        cli_change_password(self.user, self.username, self.new_password)
        self.assertFalse(self.user.check_password(self.password))

    def test_new_password_working(self):
        cli_change_password(self.user, self.username, self.new_password)
        self.assertTrue(self.user.check_password(self.new_password))


class TestOutputExtractor(TestCase):
    """
    Tests the output_extractor function
    output_extractor(response_object, format_parameter)
    It accepts either a drf Response object along with format_parameter = json
    Or a django HttpResponse with format_parameter = csv
    Test Data:
     - test-cli/test_data/csv_response_data.txt
     - 'test-cli/test_data/json_response_data.json'
    """
    def setUp(self) -> None:
        """
        Loads the appropriate data on the corresponding variables
        These files are created by the backend functions and contain the raw data that are used to generate Response
        objects
        """
        self.csv_path = 'test-cli/test_data/csv_response_data.txt'
        self.json_path = 'test-cli/test_data/json_response_data.json'
        with open(self.json_path, 'r') as f:
            self.json_response = json.load(f)
        with open(self.json_path, 'r') as f:
            self.csv_response = f.read()

    def test_json_response(self):
        """
        Test that when a DRF Response object is passed along with format_parameter='json' the returned data is correct
        """
        test_response = Response(self.json_response)
        ret = output_extractor(test_response, format_parameter='json')
        self.assertJSONEqual(json.dumps(ret), self.json_response)

    def test_csv_response(self):
        """
        Test that when an HttpResponse object is passed along with format_parameter='csv' the returned data is correct
        """
        http_response = HttpResponse(self.csv_response)
        ret = output_extractor(http_response, format_parameter='csv')
        self.assertEqual(self.csv_response, ret)


class TestValidDateFormat(TestCase):
    """
    Tests the valid_date_format function
    valid_date_format(d)
    """
    def setUp(self) -> None:
        """
        Setup correct and wrong dates
        """
        self.correct_date = '20200101'
        self.wrong_date = '2020-01-01'

    def test_wrong_date_format(self):
        """
        Test that an exception is thrown in case of a wrong date format
        """
        try:
            valid_date_format(self.wrong_date)
            self.assertTrue(False, 'No exception was thrown for wrong date format')
        except ArgumentTypeError:
            self.assertTrue(True)

    def test_correct_date_format(self):
        """
        Test that no exception is thrown in case of correct date format
        """
        try:
            valid_date_format(self.correct_date)
            self.assertTrue(True)
        except ArgumentTypeError:
            self.assertTrue(False, 'An exception was thrown for correct date format')

    def test_correct_date_is_returned(self):
        """
        Test that the date is returned as it is without any modifications in case of no error
        """
        ret = valid_date_format(self.correct_date)
        self.assertEqual(ret, self.correct_date)


class TestValidUsernameFormat(TestCase):
    """
    Tests the valid_date_format function
    valid_date_format(d)
    """
    def setUp(self) -> None:
        """
        Setup correct and wrong usernames and the expected return value following iso-8859-1
        """
        self.correct_username = 'ParserTestUsername'
        self.wrong_username = 'Δεν είναι δεκτό'
        self.correct_return = self.correct_username

    def test_wrong_username_format(self):
        """
        Test that an exception is thrown in case of a wrong username format
        """
        try:
            valid_username_format(self.wrong_username)
            self.assertTrue(False, 'No exception was thrown for wrong username format')
        except:
            self.assertTrue(True)

    def test_correct_date_format(self):
        """
        Test that no exception is thrown in case of correct username format
        """
        try:
            valid_username_format(self.correct_username)
            self.assertTrue(True)
        except ArgumentTypeError:
            self.assertTrue(False, 'An exception was thrown for correct username format')

    def test_correct_date_is_returned(self):
        """
        Test that the date is returned as it is without any modifications in case of no error
        """
        ret = valid_username_format(self.correct_username)
        self.assertEqual(ret, self.correct_return)


class TestHealthCheckCli(TestCase):
    """
    Tests that the parser works when used with the healthcheck argument
    Test Data:
     - test-cli/test_data/healthcheck_csv.txt
     - test-cli/test_data/healthcheck.json
     - test-cli/test_data/healthcheck_no_format.txt
    """
    def setUp(self) -> None:
        self.csv_output_args = ['healthcheck', '--format', 'csv']
        self.json_output_args = ['healthcheck', '--format', 'json']
        self.no_format_args = ['healthcheck']
        (self.main_parser, self.admin_parser) = setup_main_parser()
        self.csv_output_path = 'test-cli/test_data/healthcheck_csv.txt'
        with open(self.csv_output_path, 'r') as f:
            self.expected_csv_output = f.read().rstrip()
        self.json_output_path = 'test-cli/test_data/healthcheck.json'
        with open(self.json_output_path, 'r') as f:
            self.expected_json_output = json.load(f)
        self.no_format_output_path = 'test-cli/test_data/healthcheck_no_format.txt'
        with open(self.no_format_output_path, 'r') as f:
            self.expected_no_format = f.read().rstrip()

    def test_healthcheck_cli_csv(self):
        x = self.main_parser.parse_args(self.csv_output_args)
        f = io.StringIO()
        with redirect_stdout(f):
            x.func(x)
        s = f.getvalue()
        self.assertEqual(s.rstrip(), self.expected_csv_output)

    def test_healthcheck_cli_json(self):
        x = self.main_parser.parse_args(self.json_output_args)
        f = io.StringIO()
        with redirect_stdout(f):
            x.func(x)
        s = f.getvalue()
        self.assertJSONEqual(json.dumps(self.expected_json_output), s)
