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
    #stages = []
    stageInfo = []
    stageIndex = -1
    for line in dataFileContents.split("\n"):
        i += 1
        if i == 1:
            continue

        #This means Stage Info
        if len(line) > 0 and line[0] == ",":
            si = int(line[1:].split("\\")[0])
            if si >= -1:
                stageIndex += 1
                info = line[1:].split("\\")[1:]
                stageInfo.append(info)
                #stages.append([])
                print "Reading Stage " + str(stageIndex)
            continue
        
        data = line.split(", ")
        if(len(data) < 9):
            continue
        if stageIndex == 0:
            entries += 1
        #    0               1            2                  3                 4           5     6
        #position + ", " + name + ", " + playerID + ", " + vehicle + ", " + time + ", " + diff, nationIMG
        #tout += "<tr><td>" + data[0] + "</td><td>" + data[1] + "</td><td>" + data[3] + "</td><td>" + data[4] + "</td><td>" + data[5] + "</td><td>" + platform + "</td></tr>\n"

        t = data[4]
        seconds = 0.0
        if t.count(":") == 1:
            seconds += int(t.split(":")[0]) * 60.0
        elif t.count(":") == 2:
            seconds += int(t.split(":")[0]) * 60.0 * 60.0
            seconds += int(t.split(":")[1]) * 60.0
        if t.count(":") == 0:
            seconds = float(t)
        else:
            seconds += float(t.split(":")[-1])
        
        tout.append((data[1], data[3], data[4], platform, data[6], data[7], data[8], stageIndex, data[2], seconds))
        #entries += 1
    return (tout, entries, stageInfo)

bfn = "results/" + sys.argv[2] + "/data/" + sys.argv[1] + "_"

dfUrl = bfn + "steam" + ".txt"
fileTime = os.path.getmtime(dfUrl)


dataFile = open(dfUrl, "r")
dataFileContents = dataFile.read()
dataFile.close()

templateFile = open("template.html", "r")
template = templateFile.read()
templateFile.close()



out = template + ""

eventInfo = dataFileContents.split("\n")[0].split("\\")
#0          1              2               3                  4        5                6               7                  8         9
#name +  + numStages +  + location +  + locationImage +  + stage +  + stageImage +  + timeOfDay +  + weatherImage +  + weather +  + numEntries + + eventDate




combined = []

numEntries = 0

#stages = []

d,e,stageInfo = getTableData(bfn + "steam" + ".txt", "Steam")
combined.extend(d)
#stages.extend(d)
numEntries += e

d,e,s2 = getTableData(bfn + "psn" + ".txt", "PS4")
combined.extend(d)
#stages.extend(d)
numEntries += e

d,e,s2 = getTableData(bfn + "live" + ".txt", "Xbox")
combined.extend(d)
#stages.extend(d)
numEntries += e

d,e,s2 = getTableData(bfn + "oculus" + ".txt", "Oculus")
combined.extend(d)
#stages.extend(d)
numEntries += e

print str(numEntries) + " entries over " + str(len(stageInfo)) + " stages"



out = template.replace("%file_time%", str(fileTime)).replace("%title%", "DiRT Cross Platform Results Import").replace("%info%", eventInfo[0] + ", " + sys.argv[1] + "<br>" + str(numEntries) + " Entries, " + str(max(1, len(stageInfo)-1)) + " Stage(s)<br>")
#<img src='http://dirtgame.com" + eventInfo[3] + "'></img><img src='http://dirtgame.com" + eventInfo[7] + "'></img>

#overall = stages[0]

#              0        1         2         3        4          5        6     7
#tout.append((data[1], data[3], data[4], platform, data[6], data[7], data[8], stageIndex))
overall = []
for entry in combined:
    if(entry[7] == 0):
        overall.append(entry)

numStages = len(stageInfo)

table = '<table class="tablesorter"><thead><tr><th>#</th><th>Driver</th><th>Vehicle</th>'

for i in range(1,len(stageInfo)):
    table += '<th>SS' + str(i) + '</th>'

table += '<th>Total Time</th><th>Diff. First</th><th>Platform</th></tr></thead><tbody>'

overall.sort(key=operator.itemgetter(9))

pos = 1

fastestTimeS = overall[0][2].split(".")[0]
fastestTimeMS = int(overall[0][2].split(".")[1])
fastestTimeF = "%H:%M:%S"
if fastestTimeS.count(":") == 1:
    fastestTimeF = "%M:%S"
elif fastestTimeS.count(":") == 0:
    fastestTimeF = "%S"
fastestTimeT = datetime.datetime.strptime(fastestTimeS, fastestTimeF)


def getDiff(a, b):
    a_s = a.split(".")[0]
    b_s = b.split(".")[0]
    a_ms = int(a.split(".")[1])
    b_ms = int(b.split(".")[1])

    a_f = "%H:%M:%S"
    if a_s.count(":") == 1:
        a_f = "%M:%S"
    elif a_s.count(":") == 0:
        a_f = "%S"
    a_t = datetime.datetime.strptime(a_s, a_f)

    b_f = "%H:%M:%S"
    if b_s.count(":") == 1:
        b_f = "%M:%S"
    elif b_s.count(":") == 0:
        b_f = "%S"
    b_t = datetime.datetime.strptime(b_s, b_f)

    delta = b_t - a_t

    s = delta.seconds
    if(b_ms < a_ms):
        s -= 1
    
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    diff = ""
    if hours > 0:
        diff += str(hours) + ":"
    if minutes > 0:
        diff += str(minutes) + ":"
    else:
        diff += "00:"
    if len(str(seconds)) == 1:
        diff += "0"
    diff += str(seconds) + "."
    msd = b_ms - a_ms
    if msd < 0:
        msd = 1000 + msd
    diff += str(msd)
    diff += "0" * (3 - len(str(msd)))

    return diff


for item in overall:
    #print item[8]
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
    
    nin = "<img src='http://dirtgame.com" + item[4] + "'></img>&nbsp;"
    ni = ""
    if item[5] == "True":
        ni += "<img src='http://dirtgame.com/content/images/leaderboard/icon_founder.png'></img>&nbsp;"
    if item[6] == "True":
        ni += "<img src='http://dirtgame.com/content/images/leaderboard/icon_vip.png'></img>"
    
    #table += "<tr><td>" + str(pos) + "</td><td>" + ni + "</td><td>" + item[0] + "</td><td>" + item[1] + "</td><td>" + item[2] + "</td><td>" + diff + "</td><td>" + item[3] + "</td></tr>\n"

    ltable = "<tr><td>" + str(pos) + "</td><td>" + nin + item[0] + ni + "</td><td>" + item[1] + "</td>"
    pid = item[8]
    partStages = 0
    prevTime = "0.0"
    for entry in combined:
        if int(entry[7]) > 0 and entry[8] == pid:
            #print entry[7]
            partStages += 1
            ltable += "<td>" + getDiff(prevTime, entry[2]) + "</td>"
            prevTime = entry[2]
    #table += "<td></td>" * (partStages - (numStages-1))
    
    #Overall stuff
    ltable += "<td>" + item[2] + "</td><td>" + diff + "</td><td>" + item[3] + "</td></tr>\n"

    if not partStages == len(stageInfo) - 1:
        continue
    table += ltable
    pos += 1

table += "</tbody></table>"

out = out.replace("%table%", table)

outFile = open("results/" + sys.argv[2] + "/" + sys.argv[1] + ".html", "w")
outFile.write(out)
outFile.close()
