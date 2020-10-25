"""Flask API."""
from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer
from math import floor
import random
from Google import Create_Service
import datetime
from pprint import pprint
from flask_cors import CORS
from manageDay import get_schedule
from flask import Flask
from flask import request, jsonify
import copy
from collections import defaultdict
app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)

# postgres://momdad@wise-cougar-5x2.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=./wise-cougar-ca.crt


CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
allEvents = []
nameToId = defaultdict(list)
endTime = ""

# Base = declarative_base()
# engine = create_engine(
#     'cockroachdb://momdad:momdadmomdad@wise-cougar-5x2.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=./wise-cougar-ca.crt', echo=True)


# class Event(Base):
#     __tablename__ = 'schedules'
#     id = Column(Integer, primary_key=True)
#     eventName = Column(String)
#     start = Column(String)
#     end = Column(String)


# Base.metadata.create_all(engine)

seen_ids = set()


def create_sch(sess, schedule):
    new_events = []
    billion = 1000000000
    for event in schedule:
        new_id = floor(random.random()*billion)
        seen_ids.add(new_id)
        new_events.append(
            Event(
                id=new_id,
                eventName=event[0],
                start=event[1],
                end=event[2])
        )
    sess.add_all(new_events)

# def get_random_account_id():
#     """ Helper function for getting random existing account IDs.
#     """
#     random_id = random.choice(tuple(seen_ids))
#     return random_id

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/event-manager', methods=['POST'])
def index():
    data = request.get_json()
    t = []
    startTime = data['start']
    global endTime
    endTime = data['end']
    for event in data['events']:
        t.append((event['eventName'], event['start'], event['end'],
                  event['priority'], event['fixed'], event['duration']))

    global allEvents
    allEvents = copy.deepcopy(t)

    print(t)
    bestSchedule = get_schedule(t, startTime, endTime)
    # bestSchedule = [("math", "06:00", "07:00"), ("english", "10:00", "13:00")]
    for event in bestSchedule:
        addEvent(event[1], event[2], event[0])
    print(bestSchedule)
    # deleteEvent("math")
    # deleteEventsAfterTime("10:30")
    # run_transaction(sessionmaker(bind=engine),
    #                 lambda s: create_sch(s, bestSchedule))

    return jsonify(bestSchedule)


@app.route('/shift', methods=['POST'])
def index2():
    data = request.get_json()
    return jsonify(deleteAllandCreateNew(data['delay']))


def addEvent(startD, endD, title):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    startDate = '2020-10-25T' + startD + ':00-05:00'
    # -05:00 is the time zone (Central)
    endDate = '2020-10-25T' + endD + ':00-05:00'

    name = title
    event = {
        'summary': name,
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
    nameToId[title].append(event['id'])


# def editEvent(name, startTime, endTime):
#     event = service.events().get(calendarId='primary', eventId=nameToId[name]).execute()
#     startDate = '2020-10-24T' + startTime + ':00-05:00'
#     endDate = '2020-10-24T' + endTime + ':00-05:00' #-05:00 is the time zone (Central)

#     event['start']['dateTime'] = startDate
#     event['end']['dateTime'] = endDate

#     updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()


def deleteEvent(name, time):
    if name in nameToId:
        for id1 in nameToId[name]:
            eventSDKFH = service.events().get(calendarId='primary', eventId=id1).execute()
            startTime = eventSDKFH['end']['dateTime'][11:16]
            if lessThanEqualTo(startTime, time):
                service.events().delete(calendarId='primary', eventId=id1).execute()
                print("deleting ", name, id1)
                nameToId[name].remove(id1)

        if len(nameToId[name]) == 0:
            del nameToId[name]

# to help generate new shifted schedule


def deleteEventsBeforeTime(time):
    d2 = copy.deepcopy(nameToId)
    for k, v in d2.items():
        # event = service.events().get(calendarId='primary', eventId=id1).execute()
        # print(event['start']['dateTime'][11:16])
        deleteEvent(k, time)
    print("idToName", nameToId)


def lessThanEqualTo(time1, time2):
    t1 = int(time1[:2])*60 + int(time1[-2:])
    t2 = int(time2[:2])*60 + int(time2[-2:])

    if t1 <= t2:
        return True

    return False


def deleteAllandCreateNew(time):
    deleteEventsBeforeTime(time)
    for i, j in nameToId.items():
        for id1 in j:
            service.events().delete(calendarId='primary', eventId=id1).execute()
    global allEvents
    t = []
    for event in allEvents:
        if event[0] in nameToId:
            if event[1] == "" or not lessThanEqualTo(event[1], time):
                t.append(event)
    print("t", t)
    allEvents = t
    newSchedule = get_schedule(t, time, endTime)

    for event in newSchedule:
        addEvent(event[1], event[2], event[0])
    print(newSchedule)
    return newSchedule


if __name__ == '__main__':
    app.run()
