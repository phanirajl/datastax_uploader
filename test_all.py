#!/usr/bin/python3
import os
import unittest
from datetime import datetime
from pdb import set_trace

from app import URI
from app import app as flask_app


class FlaskGetUrlTests(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()
        self.mockfile = './mockfile'


    def test_get_url(self):
        """ This should validate '/' endpoint with all the validation steps, e.g
            before_request, after_request, version validation and etc.
        """
        response = self.app.post('/')
        json = response.json
        timestamp = json.get('timestamp', None)

        self.assertTrue(response.status_code == 200)
        self.assertTrue(json.get('id', None))
        self.assertTrue(json.get('upload_uri', None))
        self.assertTrue(timestamp)
        self.assertTrue(json['upload_uri'].endswith(json['id']))
        self.assertTrue(datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S %Z"))


if __name__ == '__main__':
    unittest.main()
