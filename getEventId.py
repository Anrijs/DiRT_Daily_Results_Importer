import os
import sys
import requests

test = requests.get("https://www.dirtgame.com/uk/events").text
for line in test.split("\n"):
    if line.startswith('<select data-ng-model="eventId" id="daily_prevEvents" name="daily_prevEvents"'):
        print "Found Event Stuff!"
        #<select data-ng-model="eventId" id="daily_prevEvents" name="daily_prevEvents"><option value="138139">Current event</option>
        eventId = line[(line.find('<option value="') + 15):(line.find('">Current event</option>'))]
        print eventId
        break
