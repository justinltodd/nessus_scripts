#!/usr/bin/python

######################################
#
# 
# CREATED BY JUSTIN TODD
# NESSUS API (XMLRPC) INTERACTION
# DATE: 04/28/2016
#
#
#
#######################################

try:import requests
except: print('Need to install the Requests module before execution'); exit()
import getpass
import json
import sys
import os
import atexit
import time
import argparse
import collections
from tabulate import tabulate
from prettytable import PrettyTable

################################################################################
# CHECK VERSION OF PYTHON 2.x OR GREATER IF NOT EXIT
current_maj_version = sys.version_info.major
if current_maj_version != 2:
    print('This script must be run with Python version 2.x')
    exit()

################################################################################

# DISABLE WARNING WHEN NOT VERIFYING SSL CERTS.
requests.packages.urllib3.disable_warnings()

class SSLException(Exception):
    pass

class create_menu:
    '''This is used to build an instance of the menu object
       and can be called from the main program to instantiate the menu
       with passed variables.'''
    def __init__(self, menu, text, other):
        self.text = text
        self.menu = menu
        self.other = other
	# Build the menu
        option_length_menu = len(menu)
        option_length_text = len(text)
        if self.other != 'Null':
            #print('%s' + (20-option_length_menu) * '\t' + '  :  %s' + (15-option_length_text)*'\t' +  ':    %s').expandtabs(10) %(menu,text,other)
	    #print tabulate([["Scan Name", "Status","ID"],['%s','%s','%s']], tablefmt="grid") %(menu,text,other)
	    print tabulate([['%s','%s','%s']], tablefmt="plain") %(menu,text,other)
        else:
            print('%s' + (15-option_length_menu) * ' ' + '  :  %s') %(menu,text)
        return

################################################################################

def build_url(resource):
    return '{0}{1}'.format(url, resource)

################################################################################

def connect(method, resource, data=None, params=None):
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
        r = requests.get(build_url(resource), params=params, headers=headers, verify=verify)

    # EXIT IF THERE IS AN ERROR.
    if r.status_code != 200:
        e = r.json()
        print e['error']
        sys.exit()

    # WHEN DOWNLOADING A SCAN NEED THE ROW CONTENTS NOT THE JSON DATA.
    if 'download' in resource:
        return r.content

    # ALL OTHER RESPONSES SHOULD BE JSON. RETURN RAW CONTENT IF THEY ARE NOT
    try:
        return r.json()
    except ValueError:
        return r.content

################################################################################

def login(usr, pwd):
        # LOGIN TO NESSUS 6

        login = {'username': usr, 'password': pwd}
        data = connect('POST', '/session', data=login)
        return data['token']


################################################################################

def get_policies():
    """
    Get scan policies
    Get all of the scan policies but return only the title and the uuid of
    each policy.
    """
    data = connect('GET', '/editor/policy/templates')
    return dict((p['title'], p['uuid']) for p in data['templates'])

################################################################################

def get_scans():
    """
    Get history ids
    Create a dictionary of scans and uuids
    """

    data = connect('GET', '/scans/')
    status_dict = dict((p['name'], p['status']) for p in data['scans'])
    id_dict = dict((b['name'], b['id']) for b in data['scans'])

    return status_dict, id_dict

################################################################################

def get_history_ids(sid):
    """
    Get history ids
    Create a dictionary of scan uuids and history ids so we can lookup the
    history id by uuid.
    """
    data = connect('GET', '/scans/{0}'.format(sid))
    temp_hist_dict = dict((h['history_id'], h['status']) for h in data['history'])
    temp_hist_dict_rev = {a:b for b,a in temp_hist_dict.items()}
    try:
        for key,value in temp_hist_dict_rev.items():
            print key
            print value
    except:
        pass
    #return dict((h['uuid'], h['history_id']) for h in data['history'])

################################################################################

def get_scan_history(sid, hid):
    """
    Scan history details
    Get the details of a particular run of a scan.
    """
    params = {'history_id': hid}
    data = connect('GET', '/scans/{0}'.format(sid), params)
    return data['info']

################################################################################

def get_status(sid):
    # GET THE STATUS OF THE SCAN BY THE SID.
    # PRINT OUT THE SCAN STATUS

    time.sleep(3) # SLEEP TO ALLOW NESSUS TO PROCESS THE PREVIOUS STATUS CHANGE
    temp_status_dict, temp_id_dict = get_scans()
    print '\nScan Name           Status  '
    print '---------------------------------------'
    for key, value in temp_id_dict.items():
        if str(value) == str(sid):
            create_menu(key, temp_status_dict[key], 'Null')

################################################################################

def launch(sid):
    # RESUME THE SCAN SPECIFIED BY THE SID

    data = connect('POST', '/scans/{0}/launch'.format(sid))
    return data['scan_uuid']

def pause(sid):
    # RESUME THE SCAN SPECIFIED BY THE SID
    connect('POST', '/scans/{0}/pause'.format(sid))
    return

def resume(sid):
    # RESUME THE SCAN SPECIFIED BY THE SID
    connect('POST', '/scans/{0}/resume'.format(sid))
    return

def stop(sid):
    # RESUME THE SCAN SPECIFIED BY THE SID
    connect('POST', '/scans/{0}/stop'.format(sid))
    return

def logout():
    # LOGOUT OF NESSUS
    print('Logging Out...')
    connect('DELETE', '/session')
    print('Logged Out')
    exit()

################################################################################

## MAIN - GET CREDENTIALS ##
print "\nNessus 6 API 1.0\n" 

# GET SERVER URL or IP ADDRESSs
url = raw_input("\nEnter the Nessus Server URL/IP:PORT : ")
#print "you entered", url

verify = False
token = ''

# GET PORT
#port = raw_input("\nEnter the Nessus Server Port [443]: ")
#if not port:
#	port = 443			

#print "you entered", port

# COLLECT USER/PASS INFO
username = raw_input("\nEnter your Nessus Username: ")
#print "you entered", username


password = getpass.getpass("\nEnter your Nessus Password (will not echo): ")
#print "you entered\n", password  ## TEMPORARY

if __name__ == '__main__':
	print('Logging in...')
	try:token = login(username, password)
	except: print('Unable to login :('); exit()
	print('Logged in!\n\n')

################################################################################

## Text menu in Python
      
def print_menu():       ## Your menu design here
    print 30 * "-" , "MENU" , 30 * "-"
    print "1. List All Scan" ###### Display all scans  #######
    print "2. Menu Option 2"
    print "3. Menu Option 3"
    print "4. Menu Option 4"
    print "5. Exit"
    print 67 * "-"
  
loop=True      
  
while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = input("Enter your choice [1-5]: ")
     
    if choice==1:
        print "Menu 1 has been selected"

	temp_status_dict, temp_id_dict = get_scans()
        print 'Scan Name                  Status              ID'
        print '-------------------------------------------------'

        for status_name,status in temp_status_dict.items():
            for id_name, id in temp_id_dict.items():
                if status_name == id_name:
                    create_menu(status_name,status, id)

        ## You can add your code or functions here
    elif choice==2:
        print "Menu 2 has been selected"
        ## You can add your code or functions here
    elif choice==3:
        print "Menu 3 has been selected"
        ## You can add your code or functions here
    elif choice==4:
        print "Menu 4 has been selected"
        ## You can add your code or functions here
    elif choice==5:
        logout()
        print "Logged Out"
        ## You can add your code or functions here
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Wrong option selection. Enter any key to try again..")

'''
# https object
http = Net::HTTP.new(nserver, nserverport)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

# login and get token cookie
headers = get_token(http, username, password)
'''
