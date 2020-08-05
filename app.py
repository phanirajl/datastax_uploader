#!/usr/bin/python3
"""
The goal of this exercise is to create a service that allows a user to upload an
asset and then request a time expiring URL to retrieve that asset.

Extra Credit: Is this service production ready? Why or why not? What would you need
to make it production ready?

Not ready for production, for the following reasons:
 - Needs to be refactored into the Object Oriented structure. Not implemented that
 way from the start, because this is Not intended for production from the start,
 thus, for simplicity, the procedural approach was chosen.

 - Need more verification/clarification on requirements. E.g. are multiple file
 uploads allowed? Limit on file size? How do we sync or clean up uploaded files?

 - Security applications are not fully investigated and no-to-little safety measures
 are taken.
"""
import os
import uuid
from datetime import datetime, timedelta

import flask


app = flask.Flask('datastax_uploader')
URI = {} #FIXME: this should be saved into real DB for production


def sync(assets):
    """
        Loop through files in the ASSETS_DIR folder and update the URI date with
    the name and timestamp (converted to datetime obj)
    """
    for root, _, files in os.walk(assets):
        for f in files:
            path = os.path.join(root, f)
            URI[f] = {
                'timestamp': datetime.fromtimestamp(os.path.getatime(path)),
                'file_path': path,
            }


def is_timeout(id):
    """
        Check the time difference between Now and the time of created asset. By
    default, assumes 60 sec as a timeout.

    @return: None if id does not exist (e.g. no file found), True if file created
            more than 60 seconds ago. False otherwise.
    """
    if id not in URI: return None

    timeout = URI[id]['timestamp'] + timedelta(seconds=app.config.get('URI_TIMEOUT', 60))
    return (datetime.now() - timeout).days >= 0


def clean_up(id):
    """
        Remove the physical file from the assets folder. Make few assumption and
    validations to do so to prevent from removing anything that is not assets.
    """
    if id not in URI: return

    filepath = URI[id].get('filepath', None)
    # make sure exists and is a file (semi-security. to prevent removing / and such)
    if not os.path.isfile(filepath): return

    # Semi-Security. Make sure removing file from the ASSETS
    if not filepath.startswith(app.config['ASSETS_DIR']): return
    os.remove(filepath)


@app.route('/', methods=('POST',))
def get_upload_url():
    """
        Generate a unique ID and return a uri path for user to use to upload a
    file to.
    """
    resp = {}
    id = uuid.uuid1().hex
    resp['id'] = id

    timestamp = datetime.now() # time of request
    upload_uri = '{base}upload/{id}'.format(
        base=flask.request.url_root,
        id=id
        )
    URI[id] = {}
    # move uri prefix to a variable in config or something
    URI[id]['path'] = upload_uri
    URI[id]['timestamp'] = timestamp
    resp['timestamp'] = timestamp
    resp['upload_uri'] = upload_uri
    return flask.make_response(resp, 200)


@app.route('/upload/<id>', methods=('PUT',))
def upload_asset(id):
    """
        Take the attached by the user file and save it into the assets folder while
    setting the timeout value.

    @return: json obj with info where to download the file.
    """
    global URI
    resp = {}
    if id not in URI:
        resp['msg'] = 'Unknown requested upload id "%s"' % id
        return flask.make_response(resp, 406)

    if is_timeout(id):
        resp['msg'] = 'Requested uri has expired!'
        clean_up(id)
        return flask.make_response(resp, 408)

    if not flask.request.content_length:
        resp['msg'] = "No asset found in body."
        return flask.make_response(resp, 406)

    if int(flask.request.content_length) > 20000: # FIXME: any restriction on file size?
        resp['msg'] = "Uploaded file is too big."
        return flask.make_response(resp, 413)

    if 'file' not in flask.request.files:
        resp['msg'] = "NO file found in the request!"
        return flask.make_response(resp, 418)

    file = flask.request.files['file']
    filename = os.path.basename(URI[id]['path']) # id in the path is the filename
    destination = app.config.get('ASSETS_DIR', None)
    if not destination or not os.path.exists(destination):
        resp['msg'] = 'Assets folder does not exist at %s!' % destination
        return flask.make_response(resp, 200)

    URI[id]['file_path'] = os.path.join(destination, filename)
    file.save(os.path.join(destination, filename))

    resp['msg'] = 'Uploaded file %s' % filename
    resp['download'] = '%sdownload/%s' % (flask.request.url_root, id)

    URI[id]['timestamp'] = datetime.now()
    return flask.make_response(resp, 200)


@app.route('/download/<id>', methods=('GET',))
def download_file(id):
    global app
    resp = {}
    timeout = is_timeout(id)
    if timeout is None:
        resp['msg'] = 'File at requested uri does not exist!'
        return flask.make_response(resp, 400)

    if timeout:
        resp['msg'] = 'Requested uri has expired!'
        return flask.make_response(resp, 400)

    filepath = URI[id]['file_path']
    if not os.path.exists(filepath):
        resp['msg'] = 'File does not exist!'
        return flask.make_response(resp, 500)

    return flask.send_file(filepath, as_attachment=True)


def main(args={}):
    cfg = args.get('config', {})
    app.config.update(cfg)
    sync(cfg['ASSETS_DIR'])
    app.run(
        debug=True,
        port=cfg.get('PORT', 8080),
        ssl_context='adhoc'
        )


if __name__ == '__main__':
    cfg = {
        'PORT': 8080,
        'URI_TIMEOUT': 60,
        'ASSETS_DIR': os.path.realpath('./assets')
    }
    main(args={ "config" : cfg })
