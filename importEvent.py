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
#maxPages = 2

webSession = requests.Session()


def downloadResults(eventId, platform):
    print "Doing Platform " + platform
    
    #eventDate = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
    
    dirtNumber = "10"
    initialUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=1&stageId=0&wheel=any&nameSearch="
    print "Getting Initial Event Data..."
    resp = webSession.get(initialUrl).text.encode('utf-8')
    j = json.loads(resp)
    print "Initial Data Downloaded: "

    initialSeparator = "\\"

    name = (j["EventName"]).encode('ascii',errors='ignore').replace(initialSeparator, "")
    numStages = str(j["TotalStages"]).replace(initialSeparator, "")
    location = str(j["LocationName"]).replace(initialSeparator, "")
    locationImage = str(j["LocationImage"]).replace(initialSeparator, "")
    stage = str(j["StageName"]).replace(initialSeparator, "")
    stageImage = str(j["StageImage"]).replace(initialSeparator, "")
    timeOfDay = str(j["TimeOfDay"]).replace(initialSeparator, "")
    weatherImage = str(j["WeatherImageUrl"]).replace(initialSeparator, "")
    weather = str(j["WeatherText"]).replace(initialSeparator, "")
    numPages = str(j["Pages"]).replace(initialSeparator, "")
    numEntries = str(j["LeaderboardTotal"]).replace(initialSeparator, "")

    file = open("imports/" + eventDate + "_" + platform + ".txt", "w")
    file.write(name + initialSeparator + numStages + initialSeparator + location + initialSeparator + locationImage + initialSeparator + stage + initialSeparator + stageImage + initialSeparator + timeOfDay + initialSeparator + weatherImage + initialSeparator + weather + initialSeparator + numEntries + initialSeparator + eventDate.replace(initialSeparator, "") + "\n")

    pages = int(numPages)

    for page in range(1, min(pages, maxPages)+1):
        print "Downloading Page " + str(page) + "..."
        pageUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=" + str(page) + "&stageId=" + str(numStages) + "&wheel=any&nameSearch="
        data = webSession.get(pageUrl).text.encode('utf-8')
        j = json.loads(data)
        entries = j["Entries"]
        for e in entries:
            position = str(e["Position"]).replace(",", "")
            nation = e["NationalityImage"].replace(",", "")
            playerID = str(e["PlayerId"]).replace(",", "")
            name = e["Name"].encode('ascii',errors='ignore').replace(",", "")
            vehicle = e["VehicleName"].replace(",", "")
            time = e["Time"].replace(",", "")
            diff = e["DiffFirst"].replace(",", "")

            resString = position + ", " + name + ", " + playerID + ", " + vehicle + ", " + time + ", " + diff
            file.write(resString + "\n")
            #print resString

    file.close()



#eventId = str(calibrationEvent + calibrationDelta) #"138139"
#print "Event: " + eventId
print "Date: " + eventDate

changePlatformUrl = "https://dirtgame.com/uk/changeplatform?platform=" #steam, playstationnetwork, microsoftlive, oculus

webSession.get(changePlatformUrl + "steam")
downloadResults(calibrationEvent + calibrationDelta, "steam")
webSession.get(changePlatformUrl + "playstationnetwork")
downloadResults(calibrationEvent + calibrationDelta, "psn")
webSession.get(changePlatformUrl + "microsoftlive")
downloadResults(calibrationEvent + calibrationDelta, "live")
webSession.get(changePlatformUrl + "oculus")
downloadResults(calibrationEvent + calibrationDelta, "oculus")

os.system("python createPage.py " + eventDate)
