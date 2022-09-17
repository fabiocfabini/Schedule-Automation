from pprint import pprint
from datetime import datetime
from datefinder import find_dates
from Classes import Event, EventBuilder

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

def get_duration(startDate, eStart, eEnd, eWeekDay):
    """ get duration of event

    Args:
        startDate (datetime object): start of school date.
        eStart (float): time of day the event starts (hour)
        eEnd (float): time of day the event ends (hour)
        eWeekDay (int): mapped [0,1,2,3,4] to [Monday,Tuesday, Wednesday, Thursday, Friday]

    Returns:
        string: start and end dates in isoformat  
    """
    startHour, startMinute= int(eStart), 0
    endHour, endMinute= int(eEnd), 0

    # check if event starts or ends between o'clocks
    if(eStart - startHour == 0.5): startMinute = 30
    if(eEnd - endHour == 0.5): endMinute = 30

    # this loop makes sure that the start date of the event is correct
    while(startDate.weekday() != eWeekDay):
        year = startDate.year; month = startDate.month; day = startDate.day + 1
        # New Year
        if(month == 12 and day > 31):
            year, month, day = year + 1, 1, 1
        # February special year
        elif(month == 2 and ((year % 4 == 0 and day > 29) or (year % 4 == 1 and day > 28))):
            month, day = 3, 1
        # 30/31 day months
        elif((month in [1,3,4,7,9,10] and day > 31) or (month not in [1,3,4,7,9,10] and day > 30)):
            month, day = month + 1, 1
        
        startDate = startDate.replace(day=day,month=month,year=year)

    startEvent = startDate.replace(minute=startMinute,hour=startHour).isoformat()
    endEvent = startDate.replace(minute=endMinute,hour=endHour).isoformat()

    return startEvent, endEvent

def build_event(event, startDate, endDate):
    """Creates an event corresponding to the given event

    Args:
        event (object): contains all the class information
        startDate (datetime object): start of school date.
        endDate (datetime object): end of school date.

    Returns:
        _type_: returns an Event object
    """

    newEvent = EventBuilder()

    newEvent.add_summary(event.getName())
    newEvent.add_location(event.getRoom())
    newEvent.add_description(event.getType())

    # get the start and end events in isoformat string
    startEvent, endEvent = get_duration(startDate, event.getStart(), event.getEnd(), event.getWeekDay())
    newEvent.set_duration(startEvent, endEvent)

    # format endDate as isoformat string
    endDate = endDate.isoformat()
    newEvent.set_recurrence(endDate.replace("-","").replace(":",""),FREQ = "WEEKLY")
    newEvent.set_reminders(useDefault = True)

    return newEvent