import sys
import json
import os.path
import operator
from datetime import time
import datetime
from datetime import date

def getTableData(fileName, platform):
    dataFile = open(fileName, "r")
    dataFileContents = dataFile.read()
    dataFile.close()
    entries = 0
    tout = []
    i = 0
    for line in dataFileContents.split("\n"):
        i += 1
        if i == 1:
            continue
        data = line.split(", ")
        if(len(data) < 9):
            #print "What line is this??"
            #print line
            continue
        #    0               1            2                  3                 4           5     6
        #position + ", " + name + ", " + playerID + ", " + vehicle + ", " + time + ", " + diff, nationIMG
        #tout += "<tr><td>" + data[0] + "</td><td>" + data[1] + "</td><td>" + data[3] + "</td><td>" + data[4] + "</td><td>" + data[5] + "</td><td>" + platform + "</td></tr>\n"
        tout.append((data[1], data[3], data[4], platform, data[6], data[7], data[8]))
        entries += 1
    return (tout, entries)

bfn = "imports/" + sys.argv[1] + "_"

dfUrl = bfn + "steam" + ".txt"
fileTime = os.path.getmtime(dfUrl)


dataFile = open(dfUrl, "r")
dataFileContents = dataFile.read()
dataFile.close()

templateFile = open("results/template.html", "r")
template = templateFile.read()
templateFile.close()



out = template + ""

eventInfo = dataFileContents.split("\n")[0].split("\\")
#0          1              2               3                  4        5                6               7                  8         9
#name +  + numStages +  + location +  + locationImage +  + stage +  + stageImage +  + timeOfDay +  + weatherImage +  + weather +  + numEntries + + eventDate



table = '<table class="tablesorter"><thead><tr><th>#</th><th>Nation, Founder, VIP</th><th>Driver</th><th>Vehicle</th><th>Time</th><th>Diff. First</th><th>Platform</th></tr></thead><tbody>'

combined = []

numEntries = 0

d,e = getTableData(bfn + "steam" + ".txt", "Steam")
combined.extend(d)
numEntries += e

d,e = getTableData(bfn + "psn" + ".txt", "PS4")
combined.extend(d)
numEntries += e

d,e = getTableData(bfn + "live" + ".txt", "Xbox")
combined.extend(d)
numEntries += e

d,e = getTableData(bfn + "oculus" + ".txt", "Oculus")
combined.extend(d)
numEntries += e

print str(e) + " entries"

out = template.replace("%file_time%", str(fileTime)).replace("%title%", "DiRT Daily Cross Platform Results Import").replace("%info%", eventInfo[0] + ", " + sys.argv[1] + "<br>" + eventInfo[4] + ", " + eventInfo[2] + "<br>" + eventInfo[8] + ", " + eventInfo[6] + "<br>" + str(numEntries) + " Entries, " + eventInfo[1] + " Stage(s)")


combined.sort(key=operator.itemgetter(2))

pos = 1

fastestTimeS = combined[0][2].split(".")[0]
fastestTimeMS = int(combined[0][2].split(".")[1])
fastestTimeF = "%H:%M:%S"
if fastestTimeS.count(":") == 1:
    fastestTimeF = "%M:%S"
elif fastestTimeS.count(":") == 0:
    fastestTimeF = "%S"
fastestTimeT = datetime.datetime.strptime(fastestTimeS, fastestTimeF)

for item in combined:
    
    timeS = item[2].split(".")[0]
    timeMS = int(item[2].split(".")[1])
    timeF = "%H:%M:%S"
    if timeS.count(":") == 1:
        timeF = "%M:%S"
    elif timeS.count(":") == 0:
        timeF = "%S"
    timeT = datetime.datetime.strptime(timeS, timeF)
    
    delta = timeT - fastestTimeT
    #delta = datetime.datetime.combine(date.today(), timeT) - datetime.datetime.combine(date.today(), fastestTimeT)
    
    
    s = delta.seconds
    if(timeMS < fastestTimeMS):
        s -= 1
    
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    diff = "+"
    if hours > 0:
        diff += str(hours) + ":"
    if minutes > 0:
        diff += str(minutes) + ":"
    else:
        diff += "00:"
    if len(str(seconds)) == 1:
        diff += "0"
    diff += str(seconds) + "."
    msd = timeMS - fastestTimeMS
    if msd < 0:
        msd = 1000 + msd
    diff += str(msd)
    diff += "0" * (3 - len(str(msd)))
    
    ni = "<img src='http://dirtgame.com" + item[4] + "'></img>&nbsp;"
    if item[5] == "True":
        ni += "<img src='http://dirtgame.com/content/images/leaderboard/icon_founder.png'></img>&nbsp;"
    if item[6] == "True":
        ni += "<img src='http://dirtgame.com/content/images/leaderboard/icon_vip.png'></img>"
    
    table += "<tr><td>" + str(pos) + "</td><td>" + ni + "</td><td>" + item[0] + "</td><td>" + item[1] + "</td><td>" + item[2] + "</td><td>" + diff + "</td><td>" + item[3] + "</td></tr>\n"
    pos += 1

table += "</tbody></table>"

out = out.replace("%table%", table)

outFile = open("results/" + sys.argv[1] + ".html", "w")
outFile.write(out)
outFile.close()
