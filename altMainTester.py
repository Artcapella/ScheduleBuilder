import datetime
import os.path
import random

from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#These are the global variables for the date being modified
year_global = int(2024)
month_global = int(1)
day_global = int(12)

# class for events that need to be added and then sorted
events_to_add = []

# class for events and a dictionary to hold them
event_list = []

# class for sorted events and a dictionary to hold them
sorted_event_list = []


class Event:
    def __init__(self, name, start, end, description, enjoyment, exhaustion, productivity):
        self.name = name
        self.start = start
        self.end = end
        self.description = description
        self.enjoyment = enjoyment
        self.exhaustion = exhaustion
        self.productivity = productivity

    @classmethod
    def from_adding_event(cls, adding_event, start, end):
        duration = end - start
        return cls(
            adding_event.name,
            start,
            end,
            adding_event.description,
            3,
            3,
            3
        )

class adding_event:
    def __init__(self, name, duration, description):
        self.name = name
        self.duration = duration
        self.description = description


def print_events_for_day(date):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                os.remove("token.json")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    calendar_id = "primary"
    start_time = datetime.datetime.combine(date, datetime.datetime.min.time()).isoformat() + "Z"
    end_time = datetime.datetime.combine(date, datetime.datetime.max.time()).isoformat() + "Z"


    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])

    if not events:
        print("No events found for the specified day.")
    else:
        print("Events for the day:")
        for event in events:
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            end_time = event["end"].get("dateTime", event["end"].get("date"))
            print(f"Name: {event['summary']}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print("-" * 20)

def is_event_in_calendar(event, date):
    #check the google calendar to see if there is an event with the same name
    #if there is, return true
    #if there isn't, return false (CURRENTLY RETURNS FALSE NO MATTER WHAT JUST TO TEST)
    return False


def get_events_for_day(date):

    #start of validation sequence
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                os.remove("token.json")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    #end of validation sequence

    calendar_id = "primary"
    start_time = datetime.datetime.combine(date, datetime.datetime.min.time()).isoformat() + "Z"
    end_time = datetime.datetime.combine(date, datetime.datetime.max.time()).isoformat() + "Z"


    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])

def sort_events_for_day(date):
    global event_list  # Declare event_list as a global variable

    # Copy the original event_list to avoid modifying it directly
    sorted_event_list = event_list.copy()

    # Sort the events by start time
    sorted_event_list.sort(key=lambda x: x.start)

    # Add new events to the sorted_event_list
    # Add new events to the sorted_event_list
    for adding_event in events_to_add:
        added = False
        for i, existing_event in enumerate(sorted_event_list):
            existing_event_start = datetime.datetime.strptime(existing_event.start, "%Y-%m-%dT%H:%M:%S%z")
            existing_event_end = datetime.datetime.strptime(existing_event.end, "%Y-%m-%dT%H:%M:%S%z")

            # Check if there's enough time between events
            if existing_event_end <= existing_event_start + adding_event.duration:
                new_event_start = existing_event_end
                new_event_end = existing_event_end + adding_event.duration
                new_event = Event.from_adding_event(
                    adding_event, new_event_start, new_event_end
                )
                sorted_event_list.insert(i + 1, new_event)  # Insert after the existing event
                added = True
            else:
                continue

        if not added:
            print("There is not enough time to add this event today.")




    # Reassign the sorted_event_list to event_list
    event_list = sorted_event_list

        
def user_input_flexible_event():
    print("You are adding FLEXIBLE events to: " + str(month_global) + "/" + str(day_global) + "/" + str(year_global))
    month = int(month_global)
    day = int(day_global)
    
    start_adding = input("Would you like to add a FLEXIBLE event? (y/n): ")
    if start_adding.lower() != "y":
        return()
    else:
        adding = True
    while adding:
        name = input("Enter event name")
        description = input("Enter event description: ")

        duration_minutes = int(input("Enter event duration in minutes: "))
        #convert duration to datetime format
        duration = datetime.timedelta(minutes=duration_minutes)

        #appends the global event list with the new event
        events_to_add.append(
            adding_event(name, duration, description)
        )

        continue_adding = input("Would you like to add another event? (y/n): ")
        if continue_adding.lower() != "y":
            start_adding = 'n'
            adding = False
    


def user_input_time_event():
    print("You are adding TIME SPECIFIC events to: " + str(month_global) + "/" + str(day_global) + "/" + str(year_global))
    month = int(month_global)
    day = int(day_global)
    '''
    print("What day are you adding events to?")
    month = int(input("Enter event month (1-12): "))
    day = int(input("Enter event day: "))
    '''
    start_adding = input("Would you like to add an event? (y/n): ")
    if start_adding.lower() != "y":
        return()
    else:
        adding = True
    while adding:
        time = input("Enter event start time (HH:MM): ")

        # Assuming the year is 2024.
        start_time = f"2024-{month:02d}-{day:02d}T{time}:00-07:00"

        duration_minutes = int(input("Enter event duration in minutes: "))
        end_time = (
            datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z")
            + datetime.timedelta(minutes=duration_minutes)
        )
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S%z")

        summary = input("Enter event summary: ")
        description = input("Enter event description: ")

        #appends the global event list with the new event
        event_list.append(
            Event(summary, start_time, end_time_str, description, 0, 0, 0)
        )

        continue_adding = input("Would you like to add another event? (y/n): ")
        if continue_adding.lower() != "y":
            start_adding = 'n'
            adding = False

def create_google_event(event):
    return {
        "summary": event.name,
        "location": str(","),
        "description": event.description,
        "colorId": random.randint(1, 11),
        "start": {"dateTime": event.start.isoformat(), "timeZone": "America/Denver"},
        "end": {"dateTime": event.end.isoformat(), "timeZone": "America/Denver"},
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
    }

def main():
    #start of validation sequence
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                os.remove("token.json")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    #end of validation sequence

    try:
        service = build("calendar", "v3", credentials=creds)

        print_events_for_day(datetime.date(year_global, month_global, day_global))
        '''
        #fill in the sleeping times
        event_list.append(Event("Sleeping", "2024-01-11T00:00:00-07:00", "2024-01-11T08:00:00-07:00", "Sleeping", 5, 5, 5))
        event_list.append(Event("Sleeping", "2024-01-11T00:00:00-07:00", "2024-01-11T08:00:00-07:00", "Sleeping", 5, 5, 5))
        '''

        #get events of a specific day
        date_of_events = datetime.date(year_global, month_global, day_global)  # Adjust the date as needed
        get_events_for_day(date_of_events)

        user_input_time_event()
        user_input_flexible_event()

        #sorts the events
        sort_events_for_day(date_of_events)

        for event in sorted_event_list:
            google_event = create_google_event(event)
            created_event = (
                service.events().insert(calendarId="primary", body=google_event).execute()
            )
            print("Event created: %s" % (created_event.get("htmlLink")))

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
