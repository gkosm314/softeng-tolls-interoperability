import os.path

from django.test import TestCase
from cli.commands import *
from contextlib import redirect_stdout
import io
from argparse import Namespace


# Create your tests here.

class TestOutputResponseData(TestCase):
    """
    Test the functionality of the output_response_data function
    output_response_data(response_data, format, output_path_parameter):
    """

    def setUp(self) -> None:
        self.json_response = {
            'key': 'value',
            'PassesList': [
                {
                    'pk': 1,
                    'val': 2,
                },
                {
                    'pk': 2,
                    'val': 2,
                }
            ]
        }
        self.json_file_path = 'test-cli/test.json'

    def test_output_stdout_json(self):
        """
        Test that the output is correctly printed in the stdout
        """
        f = io.StringIO()
        with redirect_stdout(f):
            output_response_data(self.json_response, format='json', output_path_parameter='stdout')
        s = f.getvalue()
        self.assertJSONEqual(json.dumps(self.json_response), s)

    def test_output_file_json(self):
        """
         Test that the output is correctly dumped in a file
         """
        output_response_data(self.json_response, format='json', output_path_parameter=self.json_file_path)
        self.assertTrue(os.path.isfile(self.json_file_path))
        with open(self.json_file_path, 'r') as f:
            file_content = json.load(f)
        self.assertJSONEqual(json.dumps(file_content), self.json_response)

    def tearDown(self):
        """
        Delete the file if it exists so future runs are not impacted
        """
        if os.path.isfile(self.json_file_path):
            os.remove(self.json_file_path)


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
        # Error message should be on test-cli/create_user_error.txt file
        with open('test-cli/create_user_error.txt', 'r') as f:
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
