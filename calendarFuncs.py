from pprint import pprint
from datetime import datetime
from Classes import Event, Classroom

#* EVENT BODY
# event = {
#     'summary': 'Google I/O 2015',
#     'location': '800 Howard St., San Francisco, CA 94103',
#     'description': 'A chance to hear more about Google\'s developer products.',
#     'start': {
#         'dateTime': '2015-05-28T09:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'end': {
#         'dateTime': '2015-05-28T17:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#     ],
#     'attendees': [
#         {'email': 'lpage@example.com'},
#         {'email': 'sbrin@example.com'},
#     ],
#     'reminders': {
#         'useDefault': False,
#         'overrides': [
#             {'method': 'email', 'minutes': 24 * 60},
#             {'method': 'popup', 'minutes': 10},
#         ],
#     },
# }

def to_RFC_3339(Date):
    year, month, day = list(map(lambda x: int(x), Date.split("-")))

    RFC_3339_date = datetime(year,month,day).isoformat()

    return RFC_3339_date

def get_duration(startDate, eStart, eEnd, eWeekDay):
    year, month, day = list(map(lambda x: int(x),startDate.split("-")))
    startHour, startMinute= int(eStart), 0
    endHour, endMinute= int(eEnd), 0

    if(eStart - startHour == 0.5): startMinute = 30
    if(eEnd - endHour == 0.5): endMinute = 30

    while(datetime(year,month,day).weekday() != eWeekDay):
        day += 1
        # New Year
        if(month == 12 and day > 31):
            year, month, day = year + 1, 1, 1
        # February special year
        elif(month == 2 and ((year % 4 == 0 and day > 29) or (year % 4 == 1 and day > 28))):
            month, day = 3, 1
        # 30/31 day months
        elif((month in [1,3,4,7,9,10] and day > 31) or (month not in [1,3,4,7,9,10] and day > 30)):
            month, day = month + 1, 1

    startEvent = datetime(year,month,day,startHour,startMinute).isoformat()
    endEvent = datetime(year,month,day,endHour,endMinute).isoformat()

    return startEvent, endEvent

def create_event(classroom, startDate, endDate):
    newEvent = Event()

    newEvent.add_summary(classroom.getName())
    newEvent.add_location(classroom.getRoom())
    newEvent.add_description(classroom.getType())

    startEvent, endEvent = get_duration(startDate, classroom.getStart(), classroom.getEnd(), classroom.getWeekDay())
    newEvent.set_duration(startEvent, endEvent)

    endDate = to_RFC_3339(endDate)
    newEvent.set_recurrence(endDate.replace("-","").replace(":",""),FREQ = "WEEKLY")
    newEvent.set_reminders(useDefault = True)

    return newEvent