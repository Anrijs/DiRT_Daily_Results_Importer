import sys
import json
import requests
import datetime
import os

def main(argv):
    dnow = datetime.datetime.utcnow().date()
    dnow = (datetime.datetime.utcnow() - datetime.timedelta(hours=10)).date()
    eventDate = dnow.strftime("%Y-%m-%d")

    eventId = -1
    test = requests.get("https://www.dirtgame.com/uk/events").text
    for line in test.split("\n"):
        if line.startswith('<select data-ng-model="eventId" id="daily_prevEvents" name="daily_prevEvents"'):
            eventId = line[(line.find('<option value="') + 15):(line.find('">Current event</option>'))]
            break

    if eventId == -1:
        print "Could not find the daily!"
        sys.exit()

    os.system("python " + os.path.dirname(os.path.abspath(__file__)) + "/importEvent.py " + str(eventId) + " " + eventDate + " " + "daily")
    print "Daily imported"


    eventId = -1
    test = requests.get("https://www.dirtgame.com/uk/events").text
    for line in test.split("\n"):
        if line.startswith('<select data-ng-model="eventId" id="daily2_prevEvents" name="daily2_prevEvents"'):
            eventId = line[(line.find('<option value="') + 15):(line.find('">Current event</option>'))]
            break

    if eventId == -1:
        print "Could not find the daily!"
        sys.exit()

    os.system("python " + os.path.dirname(os.path.abspath(__file__)) + "/importEvent.py " + str(eventId) + " " + eventDate + " " + "daily2")
    print "Daily 2 imported"

if __name__ == "__main__":
   main(sys.argv[1:])