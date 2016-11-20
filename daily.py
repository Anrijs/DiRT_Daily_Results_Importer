import sys
import json
import requests
import datetime
import os

def main(argv):
    dnow = datetime.datetime.utcnow().date()
    dnow = (datetime.datetime.utcnow() - datetime.timedelta(hours=10)).date()

    eventDate = dnow.strftime("%Y-%m-%d")

    runDaily  = True
    runDaily2 = True
    platforms = ""

    if (len(argv) > 0):
        runDaily  = False
        runDaily2 = False
        if "daily" in argv:
            runDaily = True
        if "daily2" in argv:
            runDaily2 = True
        
        argstr = ",".join(argv)
        if "steam" in argstr:  platforms += "steam,"
        if "psn" in argstr: platforms += "psn,"
        if "live" in argstr: platforms += "live,"
        if "oculus" in argstr: platforms += "oculus,"
            


    if runDaily:
        eventId = -1
        test = requests.get("https://www.dirtgame.com/uk/events").text
        for line in test.split("\n"):
            if line.startswith('<select data-ng-model="eventId" id="daily_prevEvents" name="daily_prevEvents"'):
                eventId = line[(line.find('<option value="') + 15):(line.find('">Current event</option>'))]
                break

        if eventId == -1:
            print "Could not find the daily!"
            sys.exit()

        os.system("python importEvent.py " + str(eventId) + " " + eventDate + " " + "daily " + platforms)

        print "Daily imported"
    else:
        print "Skip Daily import"

    if runDaily2:
        eventId = -1
        test = requests.get("https://www.dirtgame.com/uk/events").text
        for line in test.split("\n"):
            if line.startswith('<select data-ng-model="eventId" id="daily2_prevEvents" name="daily2_prevEvents"'):
                eventId = line[(line.find('<option value="') + 15):(line.find('">Current event</option>'))]
                break

        if eventId == -1:
            print "Could not find the daily!"
            sys.exit()

        os.system("python importEvent.py " + str(eventId) + " " + eventDate + " " + "daily2 " + platforms)

        print "Daily imported"
    else:
        print "Skip Daily 2 import"

if __name__ == "__main__":
   main(sys.argv[1:])