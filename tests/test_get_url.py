#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

import flask_fat


class FlaskGetUrlTests(unittest.TestCase):

    def test_get_url(self):
        """ This should validate '/' endpoint with all the validation steps, e.g
            before_request, after_request, version validation and etc.
        """
        app = flask_fat.APIBaseline(self.APP_NAME, cfg=self.MOCK_CFG, bp_path=self.BP_PATH)
        app = app.app.test_client()

        response = app.get('/', headers=self.headers)

        self.assertTrue(response.status_code == 200)

        #error code without version in headers
        response = app.get('/')
        self.assertTrue(response.status_code >= 400)

        #version in headers, but no json. Response should be success.
        response = app.get('/', headers={ 'Accept' : self.headers['Accept']})
        self.assertTrue(response.status_code == 200)
