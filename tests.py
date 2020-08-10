#!/usr/bin/python3
import os
import unittest
from datetime import datetime
from pdb import set_trace
import handler
import json

class UploaderTests(unittest.TestCase):

    def setUp(self):
        self.mockfile = './mockfile'


    def test_get_url(self):
        """ This should validate '/' endpoint with all the validation steps, e.g
            before_request, after_request, version validation and etc.
        """
        return
        # response = self.app.post('/')
        # json = response.json
        # timestamp = json.get('timestamp', None)

        # self.assertTrue(response.status_code == 200)
        # self.assertTrue(json.get('id', None))
        # self.assertTrue(json.get('upload_uri', None))
        # self.assertTrue(timestamp)
        # self.assertTrue(json['upload_uri'].endswith(json['id']))
        # self.assertTrue(datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S %Z"))


    def test_upload_asset_wrong(self):
        events = {
            'queryStringParameters': { 'id': 'testfilehere' },
        }
        resp = handler.upload_asset(events, {})
        self.assertTrue(resp['statusCode'] == 404)


    def test_upload_asset(self):
        resp = handler.get_url({}, {})
        id = resp.get('body', {}).get('id', None)
        self.assertTrue(id)

        events = {
            'queryStringParameters': { 'id': id},
        }

        resp = handler.upload_asset(events, {})
        self.assertTrue(resp['statusCode'] < 300)


if __name__ == '__main__':
    unittest.main()
