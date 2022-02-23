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