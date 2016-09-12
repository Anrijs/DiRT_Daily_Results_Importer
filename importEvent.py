import sys
import json
import requests
import datetime
import os


calibrationTime = datetime.datetime.fromtimestamp(1473543981)
#calibrationDay = datetime.datetime.strptime(calibrationTime.strftime('%Y-%m-%d'), "%Y-%m-%d")
calibrationDay = calibrationTime.date()

dnow = datetime.datetime.utcnow().date()

dnow = (datetime.datetime.utcnow() - datetime.timedelta(hours=12)).date()

daysDelta = (dnow - calibrationDay).days

calibrationEvent = 138139

calibrationDelta = daysDelta

eventDate = dnow.strftime("%Y-%m-%d")


maxPages = 20000000000
maxPages = 2

webSession = requests.Session()

def getEventId():
    test = requests.get("https://www.dirtgame.com/uk/events").text
    for line in test.split("\n"):
        if line.startswith('<select data-ng-model="eventId" id="daily_prevEvents" name="daily_prevEvents"'):
            #print "Found Event Stuff!"
            #<select data-ng-model="eventId" id="daily_prevEvents" name="daily_prevEvents"><option value="138139">Current event</option>
            eventId = line[(line.find('<option value="') + 15):(line.find('">Current event</option>'))]
            #print eventId
            return eventId
    return -1

def downloadResults(eventId, platform):
    print "Doing Platform " + platform
    
    #eventDate = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
    
    dirtNumber = "10"
    initialUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=1&stageId=0&wheel=any&nameSearch="
    print "Getting Initial Event Data..."
    resp = webSession.get(initialUrl).text.encode('utf-8')
    j = json.loads(resp)
    print "Initial Data Downloaded: "

    initialSeparator = u"\\"

    name = unicode(j["EventName"]).replace(initialSeparator, "")#.encode('ascii',errors='ignore').replace(initialSeparator, "")
    numStages = unicode(j["TotalStages"]).replace(initialSeparator, "")
    location = unicode(j["LocationName"]).replace(initialSeparator, "")
    locationImage = unicode(j["LocationImage"]).replace(initialSeparator, "")
    stage = unicode(j["StageName"]).replace(initialSeparator, "")
    stageImage = unicode(j["StageImage"]).replace(initialSeparator, "")
    timeOfDay = unicode(j["TimeOfDay"]).replace(initialSeparator, "")
    weatherImage = unicode(j["WeatherImageUrl"]).replace(initialSeparator, "")
    weather = unicode(j["WeatherText"]).replace(initialSeparator, "")
    numPages = unicode(j["Pages"]).replace(initialSeparator, "")
    numEntries = unicode(j["LeaderboardTotal"]).replace(initialSeparator, "")
    
    file = open("imports/" + eventDate + "_" + platform + ".txt", "w")
    file.write((name + initialSeparator + numStages + initialSeparator + location + initialSeparator + locationImage + initialSeparator + stage + initialSeparator + stageImage + initialSeparator + timeOfDay + initialSeparator + weatherImage + initialSeparator + weather + initialSeparator + numEntries + initialSeparator + eventDate.replace(initialSeparator, u"") + u"\n").encode("utf-8"))

    pages = int(numPages)

    for page in range(1, min(pages, maxPages)+1):
        print "Downloading Page " + str(page) + "..."
        pageUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=" + str(page) + "&stageId=" + str(numStages) + "&wheel=any&nameSearch="
        data = unicode(webSession.get(pageUrl).text)#.encode('utf-8')
        j = json.loads(data)
        entries = j["Entries"]
        for e in entries:
            position = unicode(e["Position"]).replace(u",", u"")
            nation = unicode(e["NationalityImage"]).replace(u",", u"")
            playerID = unicode(e["PlayerId"]).replace(u",", u"")
            name = unicode(e["Name"]).replace(u",", u"")
            vehicle = unicode(e["VehicleName"]).replace(u",", u"")
            time = unicode(e["Time"]).replace(u",", u"")
            diff = unicode(e["DiffFirst"]).replace(u",", u"")
            isFounder = unicode(e["IsFounder"]).replace(u",", u"")
            isVIP = unicode(e["IsVIP"]).replace(u",", u"")
            
            resString = position + u", " + name + u", " + playerID + u", " + vehicle + u", " + time + u", " + diff + u", " + nation + u", " + isFounder + u", " + isVIP
            file.write((resString + u"\n").encode("utf-8"))
            #print resString

    file.close()



#eventId = str(calibrationEvent + calibrationDelta) #"138139"
#print "Event: " + eventId
print "Date: " + eventDate

changePlatformUrl = "https://dirtgame.com/uk/changeplatform?platform=" #steam, playstationnetwork, microsoftlive, oculus

eventId = getEventId()
if(eventId == -1):
    print "Couldn't find the daily! Aborting!"
    sys.exit()

print "Found Event ID: " + str(eventId)

webSession.get(changePlatformUrl + "steam")
downloadResults(eventId, "steam")
webSession.get(changePlatformUrl + "playstationnetwork")
downloadResults(eventId, "psn")
webSession.get(changePlatformUrl + "microsoftlive")
downloadResults(eventId, "live")
webSession.get(changePlatformUrl + "oculus")
downloadResults(eventId, "oculus")

os.system("python createPage.py " + eventDate)
