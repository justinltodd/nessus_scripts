import requests
import json
import sys
import os


url = 'https://54.152.179.95'
#url = 'https://cloud.tenable.com/nessus6.html#/'
verify = False
token = ''
username = 'justin.todd@cleardata.com'
password = 'P@ssw0rd123'


def build_url(resource):
    return '{0}{1}'.format(url, resource)


def connect(method, resource, data=None):
    """
    Send a request
    Send a request to Nessus based on the specified data. If the session token
    is available add it to the request. Specify the content type as JSON and
    convert the data to JSON format.
    """
    headers = {'X-Cookie': 'token={0}'.format(token),
               'content-type': 'application/json'}

    data = json.dumps(data)

    if method == 'POST':
        r = requests.post(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        r = requests.put(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        r = requests.delete(build_url(resource), data=data, headers=headers, verify=verify)
    else:
        r = requests.get(build_url(resource), params=data, headers=headers, verify=verify)

    # Exit if there is an error.
    if r.status_code != 200:
        e = r.json()
        print e['error']
        sys.exit()

    # When downloading a scan we need the raw contents not the JSON data. 
    if 'download' in resource:
        return r.content

    # All other responses should be JSON data. Return raw content if they are
    # not.
    try:
        return r.json()
    except ValueError:
        return r.content


def upload(upload_file):
    """
    File uploads don't fit easily into the connect method so build the request
    here instead.
    """
    params = {'no_enc': 0}
    headers = {'X-Cookie': 'token={0}'.format(token)}

    filename = os.path.basename(upload_file)
    files = {'Filename': (filename, filename),
             'Filedata': (filename, open(upload_file, 'rb'))}

    r = requests.post(build_url('/file/upload'), params=params, files=files,
                      headers=headers, verify=verify)

    resp = r.json()

    if r.status_code != 200:
        print(resp['error'])
        sys.exit

    return resp['fileuploaded']


def login(usr, pwd):
    login = {'username': usr, 'password': pwd}
    data = connect('POST', '/session', data=login)

    return data['token']


def logout():
    connect('DELETE', '/session')


def import_scan(filename):
    im_file = {'file': filename}

    data = connect('POST', '/scans/import', data=im_file)

    scan_name = data['scan']['name']
    print('Successfully imported the scan {0}.'.format(scan_name))


if __name__ == '__main__':
    token = login(username, password)

    filename = upload('/opt/mimi.nessus')
    import_scan(filename)

    logout()
