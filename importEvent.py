import sys
import json
import requests
import datetime
import os

folder = ""
eventDate = ""
maxPages = 20000000000
progress = {"steam":[0, 0, 0, 0],"psn":[0, 0, 0, 0],"live":[0, 0, 0, 0],"oculus":[0, 0, 0, 0]}
force = False

def printStats():
    global progress
    
    ap = 100
    bp = 100
    cp = 100
    dp = 100
    
    if progress["steam"][1] > 0:
      ap = round((progress["steam"][0] * 1.0) / progress["steam"][1] * 100)
    if progress["psn"][1] > 0:
      bp = round((progress["psn"][0] * 1.0) / progress["psn"][1] * 100)
    if progress["live"][1] > 0:
      cp = round((progress["live"][0] * 1.0) / progress["live"][1] * 100)
    if progress["oculus"][1] > 0:
      dp = round((progress["oculus"][0] * 1.0) / progress["oculus"][1] * 100)
    
    a = "steam: " + str(ap) + "%"
    a += " [" + str(progress["steam"][2]) + "/" + str(progress["steam"][3]) + "]"
    b = " psn: " + str(bp) + "%"
    b += " [" + str(progress["psn"][2]) + "/" + str(progress["psn"][3]) + "]"
    c = " live: " + str(cp) + "%"
    c += " [" + str(progress["live"][2]) + "/" + str(progress["live"][3]) + "]"
    d = " oculus: " + str(dp) + "%"
    d += " [" + str(progress["oculus"][2]) + "/" + str(progress["oculus"][3]) + "]"
    
    sys.stdout.write(a + b + c + d + "      \r")
    sys.stdout.flush()
  

def downloadResults(eventId, platform, platformURL):
    global folder
    global eventDate
    global progress
    global force
    
    ph = "[" + platform + "] "
    
    webSession = requests.Session()
    changePlatformUrl = "https://dirtgame.com/uk/changeplatform?platform=" #steam, playstationnetwork, microsoftlive, oculus
    webSession.get(changePlatformUrl + platformURL)
    
    #eventDate = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
    
    dirtNumber = "10"
    initialUrl = "https://www.dirtgame.com/uk/api/event?assists=any&eventId=" + str(eventId) + "&group=all&leaderboard=true&noCache=0&number=" + str(dirtNumber) + "&page=1&stageId=0&wheel=any&nameSearch="
    resp = webSession.get(initialUrl).text.encode('utf-8')
    j = json.loads(resp)
    
    initialSeparator = u"\\"
    numStages = unicode(j["TotalStages"]).replace(initialSeparator, "")
    name = unicode(j["EventName"]).replace(initialSeparator, "")
    if int(numStages) == 1:
        numStages = "0"
    fname = eventDate + "_" + platform + ".txt"
    fpath = "results/" + folder + "/data/" + fname
    if os.path.isfile(fpath):
        if force:
            print "Overwriting " + fname  
        else:
            print "Skipping. " + fname + " already exists. Use force parameter to overwrite"
            return
    file = open(fpath, "w")
    file.write((name + u"\n").encode("utf-8"))

    progress[platform][3] = int(numStages)
    
    for stageIndex in range(-1, int(numStages)):
        progress[platform][2] = stageIndex+1
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
        
        progress[platform][1] = pages
        
        for page in range(1, min(pages, maxPages)+1):
            progress[platform][0] = page
            printStats()
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
    global force
    if (len(argv) < 3):
        print "Missing arguments."
        print "Usage: python importEvent.py eventId date-string folder [force]"
        sys.exit("")

    folder = argv[2]
    eventDate = argv[1]
    
    if "force" in argv:
      force = True

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

    print "\n"
    print "All threads joined!"

if __name__ == "__main__":
    main(sys.argv[1:])