class Classroom:

    # Class Variables
    workDays = ['Monday','Tuesday','Wednesday','Thursday','Friday']

    # Construct
    def __init__(self,name="",room="",type="",start=0,end = 0,weekday=0):
        self.name = name
        self.room = room
        self.type = type
        self.start = float(start)
        self.end = float(end)
        self.weekday = int(weekday)
    
    # Getters
    def getName(self):
        return self.name
    def getRoom(self):
        return self.room
    def getType(self):
        return self.type
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def getWeekDay(self):
        return self.weekday

    # Setters
    def setName(self,name):
        self.name = name
    def setRoom(self,room):
        self.room = room
    def setType(self,type):
        self.type = type
    def setStart(self,start):
        self.start = start
    def setEnd(self,end):
        self.end = end
    def setWeekDay(self,weekDay):
        self.weekday = weekDay

    def __str__(self):
        return "( " + str(self.name) + " , " + str(self.room) + " , " + str(self.type) + " , " + str(self.end-self.start) + "h, " + Classroom.workDays[self.getWeekDay()] + " )"

class Event:

    def __init__(self):
        self.event = {}

    def add_summary(self,summary):
        self.event['summary'] = summary

    def add_location(self,location):
        self.event['location'] = location

    def add_description(self,description):
        self.event['description'] = description

    def set_duration(self,start,end,timezone="Europe/Lisbon"):
        self.event['start'] = {}
        self.event['end'] = {}
        self.set_start_datetime(start)
        self.set_end_datetime(end)
        self.set_timezone(timezone)

    def set_recurrence(self,endDate,FREQ="WEEKLY"):
        self.event['recurrence'] = [f'RRULE:FREQ={FREQ};UNTIL={endDate+"Z"}']

    def set_reminders(self,useDefault = True):
        self.event['reminders'] = {}
        self.event['reminders']['useDefault'] = useDefault

    def set_start_datetime(self,start):
        self.event['start']['dateTime'] = start

    def set_end_datetime(self,endDate):
        self.event['end']['dateTime'] = endDate

    def set_timezone(self, timezone):
        self.event['start']['timeZone'] = timezone
        self.event['end']['timeZone'] = timezone