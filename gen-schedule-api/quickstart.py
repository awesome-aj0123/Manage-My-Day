from pprint import pprint
import datetime
from Google import Create_Service
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
startDate = '2020-10-24T09:00:00-05:00'
endDate = '2020-10-24T10:00:00-05:00' #-06:00 is the time zone (Central)

summary = "Math Class" 
event = {
    'summary': summary,
    'start': {
        'dateTime': startDate,
        'timeZone': 'America/Chicago',
    },
    'end': {
        'dateTime': endDate,
        'timeZone': 'America/Chicago',
    }
}

event = service.events().insert(calendarId='primary', body=event).execute()
# print('Event created: %s' % (event.get('htmlLink'))


# if __name__ == '__main__':
#     main()


# print('Getting the upcoming 10 events')
# events_result = service.events().list(calendarId='primary', timeMin=now,
#                                     maxResults=10, singleEvents=True,
#                                     orderBy='startTime').execute()

# events = events_result.get('items', [])



# if not events:
#     print('No upcoming events found.')
# for event in events:
#     start = event['start'].get('dateTime', event['start'].get('date'))
#     print(start, event['summary'])


# from __future__ import print_function
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# CLIENT_SECRET_FILE = 'credentals.json'

# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     service = build('calendar', 'v3', credentials=creds)

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])

