from Google import create_service
from Classes import *
from calendarFuncs import *
from get_schedule import *



CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

if __name__ == '__main__':
    classes, startDate, endDate = getScheduleData()

    for classroom in classes:
        start, end = startDate, endDate
        newEvent = build_event(classroom, start, end)

        service.events().insert(calendarId='primary', body=newEvent.event).execute()

        del newEvent

    print("\nYour schedule as been stored in the Google Calendar App. Thank you!")