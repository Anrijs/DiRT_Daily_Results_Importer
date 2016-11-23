import sys
import json
import requests
import datetime
import os

html = True
sql  = False
dl   = True
force = False

def getEvent(evtyp):
    eventId = -1
    test = requests.get("https://www.dirtgame.com/uk/events").text
    name = "";
    nl = False
    for line in test.split("\n"):
        if line.startswith('<select data-ng-model="eventId" id="' + evtyp + '_prevEvents" name="' + evtyp + '_prevEvents'):
            nl = True
            continue
        if nl == True:
            eventId = line[(line.find('<option value="') + 15):(15 + line[15:].find('">'))]
            evopt = find_between(line, "\">", "</" )
            dat = evopt.split("/")
            if (len(dat) != 3):
	        sys.exit("Error processing event: " + evopt)
            name = dat[2] + "-" + dat[1] + "-" + dat[0]
            break
    print "Event: " + eventId + " - " + name
    return eventId, name
  
def getOptions():
    if force:
        return " force"
    return ""
  
def processEvent(eventId, eventDate, eventFolder):
    global html
    global sql
    global dl
    
    if (eventId != -1):
        print "Processing " + eventFolder + " event on " + eventDate + " (" + eventId + ")"
        if dl:
            os.system("python importEvent.py " + str(eventId) + " " + eventDate + " " + eventFolder + getOptions())
        if html:
            os.system("python createPage.py " + eventDate + " " + eventFolder)
        if sql:
            os.system("python importSql.py " + eventDate + " " + eventFolder)

def daily1():
    eventId, eventDate = getEvent("daily")
    processEvent(eventId, enventDate, "daily")
  
def daily2():
    eventId, eventDate = getEvent("daily2")
    processEvent(eventId, enventDate, "daily2")

def weekly1():
    eventId, eventDate = getEvent("weekly")
    processEvent(eventId, enventDate, "weekly1")
        
def weekly2():
    eventId, eventDate = getEvent("weekly2")
    processEvent(eventId, enventDate, "weekly2")

def monthly():
    eventId, eventDate = getEvent("monthly")
    processEvent(eventId, enventDate, "monthly")

def main(argv):
    global force
    global html
    global sql
    global dl
    
    if (len(argv) == 0):
        print "Missing arguments."
        print "Usage: python run.py <event-type> [nohtml] [sql] [nodl] [force]"
        print "  event-type: daily1 daily2 weekly1 weekly2 monthly"
        sys.exit("")
    
    
    if "nohtml" in argv:
        html = False
    if "sql" in argv:
        sql = True
    if "nodl" in argv:
        dl = False
    if "force" in argv:
        force = True
       
    if "daily1" in argv:
        daily1(html,sql,dl)
    if "daily2" in argv:
        daily2(html,sql,dl)
    if "weekly1" in argv:
        weekly1(html,sql,dl)
    if "weekly2" in argv:
        weekly2(html,sql,dl)
    if "monthly" in argv:
        monthly(html,sql,dl)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

if __name__ == "__main__":
   main(sys.argv[1:])