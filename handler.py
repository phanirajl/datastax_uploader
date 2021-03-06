#!/usr/bin/python3
import json
import uuid
from datetime import datetime, timedelta
import json
from storage import Storage

RESPONSE = {
    "body": "",
    "statusCode": 100,
    "isBase64Encoded": True,
    "headers": { "Access-Control-Allow-Origin" : "*" },
}


def get_url(event, context):
    """
        Generate a unique ID and return a uri path for user to use to upload a
    file to.
    """
    resp = RESPONSE
    body = {}
    id = uuid.uuid1().hex
    body['id'] = id

    timestamp = datetime.now() # time of request
    upload_uri = '{base}?id={id}'.format(
        base='https://ow6m3i0zp0.execute-api.us-east-1.amazonaws.com/dev/get_url',
        id=id
        )

    body['timestamp'] = str(timestamp)
    body['upload_uri'] = upload_uri
    resp['statusCode'] = 200
    resp['body'] = json.dumps(body)

    Storage.upload('%s_reserved' % id, '')

    return resp


def upload_asset(event, context):
    """
        Take the attached by the user file and save it into the assets folder while
    setting the timeout value.
    @return: json obj with info where to download the file.
    """
    resp = RESPONSE
    body = {}
    resp['statusCode'] = 200
    file_obj = event.get('file', None)
    id = event.get('queryStringParameters', {}).get('id', None)

    is_exists = Storage.is_file_exists('%s_reserved' % id)
    if not is_exists:
        resp['statusCode'] = 404
        resp['message'] = 'Not a valid upload id!'
        return resp

    is_timeout = Storage.is_timeout('%s_reserved' % id)

    if is_timeout:
        resp['statusCode'] = 400
        resp['message'] ='Link timed out.'
        return resp

    body['file'] = file_obj

    Storage.upload(id, file_obj)
    return resp
