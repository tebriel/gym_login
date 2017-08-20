"""
Sheets API Interactions
"""
import os
import logging

import httplib2
import pytz
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.errors import HttpError

LOG = logging.getLogger(__name__)

# try:
#     import argparse
#     FLAGS = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     FLAGS = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
DATA_DIR = os.getenv('DATA_DIR', '/data')
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = os.path.join(DATA_DIR, 'client_secret.json')
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
LOGIN_SHEET_ID = os.getenv('LOGIN_SHEET_ID')
LOGIN_SHEET_FORM = 'Form Responses 1'
USERS_SHEET_ID = os.getenv('USERS_SHEET_ID')
USERS_SHEET_FORM = 'Sheet1'

if None in [LOGIN_SHEET_ID, USERS_SHEET_ID]:
    raise Exception("LOGIN_SHEET_ID and USERS_SHEET_ID must be set")


def get_service():
    """Gets valid service object, logged in

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Service, the service object
    """
    credential_path = os.path.join(DATA_DIR,
                                   'sheets.googleapis.com-gym_login.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # if FLAGS:
        credentials = tools.run_flow(flow, store)
        LOG.info('Storing credentials to ' + credential_path)

    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    return discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)


def add_login(login_date, login_id):
    """
    Adds a login entry to the Google Sheet
    """
    LOG.info("Seeing new login from: %s", login_id)
    eastern = pytz.timezone('US/Eastern')
    login_date = pytz.utc.localize(login_date)

    spreadsheet_id = LOGIN_SHEET_ID
    disp_date = login_date.astimezone(eastern).strftime('%m/%d/%Y %H:%M:%S')
    body = {
        'values': [[disp_date, login_id]]
    }
    value_input_option = 'USER_ENTERED'

    result = SERVICE.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=LOGIN_SHEET_FORM,
        valueInputOption=value_input_option,
        body=body)
    try:
        result.execute()
    except HttpError as httpe:
        LOG.exception('Unable to add login to sheet')
        raise httpe


def get_usernames():
    """Gets all usernames/ids from the sheet
    """
    LOG.info("Getting usernames")
    spreadsheet_id = USERS_SHEET_ID
    data = {}

    result = SERVICE.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range="{0}!A2:C".format(USERS_SHEET_FORM))
    try:
        res = result.execute()
    except HttpError:
        LOG.exception('Unable to fetch Names Data')
        return data

    for row in res.get('values', []):
        if len(row) < 3:
            # Not enough data
            continue
        data[row[2]] = "{0} {1}".format(row[0], row[1])

    return data


def get_username(login_id):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    LOG.info("Getting username for: %s", login_id)

    data = get_usernames()

    return data.get(login_id)


# Setup
SERVICE = get_service()
