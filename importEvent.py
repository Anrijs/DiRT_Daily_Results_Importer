import sys
import json
import requests
import datetime
import os

folder = ""
eventDate = ""
maxPages = 20000000000

def downloadResults(eventId, platform, platformURL):
    global folder
    global eventDate

    ph = "[" + platform + "] "
    
    print ph + "Doing Platform " + platform
    webSession = requests.Session()
    changePlatformUrl = "https://dirtgame.com/uk/changeplatform?platform=" #steam, playstationnetwork, microsoftlive, oculus
    webSession.get(changePlatformUrl + platformURL)
    
    
    #eventDate = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
    
    dirtNumber = "10"
    initialUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=1&stageId=0&wheel=any&nameSearch="
    print ph + "Getting Initial Event Data..."
    resp = webSession.get(initialUrl).text.encode('utf-8')
    j = json.loads(resp)
    print ph + "Initial Data Downloaded: "

    initialSeparator = u"\\"
    numStages = unicode(j["TotalStages"]).replace(initialSeparator, "")
    name = unicode(j["EventName"]).replace(initialSeparator, "")
    if int(numStages) == 1:
        numStages = "0"
    print ph + "Stages: " + str(numStages)
    file = open("results/" + folder + "/data/" + eventDate + "_" + platform + ".txt", "w")
    file.write((name + u"\n").encode("utf-8"))
    for stageIndex in range(-1, int(numStages)):
        stageInitUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=1&stageId=" + str(stageIndex + 1) + "&wheel=any&nameSearch="
        resp = webSession.get(stageInitUrl).text.encode('utf-8')
        j = json.loads(resp)
        
        location = unicode(j["LocationName"]).replace(initialSeparator, "")
        locationImage = unicode(j["LocationImage"]).replace(initialSeparator, "")
        stage = unicode(j["StageName"]).replace(initialSeparator, "")
        stageImage = unicode(j["StageImage"]).replace(initialSeparator, "")
        timeOfDay = unicode(j["TimeOfDay"]).replace(initialSeparator, "")
        weatherImage = unicode(j["WeatherImageUrl"]).replace(initialSeparator, "")
        weather = unicode(j["WeatherText"]).replace(initialSeparator, "")
        numPages = unicode(j["Pages"]).replace(initialSeparator, "")
        numEntries = unicode(j["LeaderboardTotal"]).replace(initialSeparator, "")
        
        
        file.write((u"," + unicode(stageIndex) + initialSeparator + location + initialSeparator + locationImage + initialSeparator + stage + initialSeparator + stageImage + initialSeparator + timeOfDay + initialSeparator + weatherImage + initialSeparator + weather + initialSeparator + numEntries + initialSeparator + eventDate.replace(initialSeparator, u"") + u"\n").encode("utf-8"))
        pages = int(numPages)

        for page in range(1, min(pages, maxPages)+1):
            print ph + "Downloading Page " + str(page) + "..."
            pageUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=" + str(page) + "&stageId=" + str(stageIndex + 1) + "&wheel=any&nameSearch="
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


#Usage: importEvent.py eventId date-string folder
def main(argv):
    global folder
    global eventDate

    folder = argv[2]
    eventDate = argv[1]

    #maxPages = 1

    print "Date: " + eventDate

    eventId = int(argv[0])
    print "Found Event ID: " + str(eventId)

    from threading import Thread
    steam = Thread(target=downloadResults, args=(eventId, "steam", "steam"))
    psn = Thread(target=downloadResults, args=(eventId, "psn", "playstationnetwork"))
    live = Thread(target=downloadResults, args=(eventId, "live", "microsoftlive"))
    oculus = Thread(target=downloadResults, args=(eventId, "oculus", "oculus"))

    print "Starting threads..."
    steam.start()
    psn.start()
    live.start()
    oculus.start()

    print "Joining threads..."
    steam.join()
    psn.join()
    live.join()
    oculus.join()

    print "All threads joined!"

    os.system("python createPage.py " + eventDate + " " + folder)

if __name__ == "__main__":
   main(sys.argv[1:])
