import sys
import json
import requests
import datetime
import os
import MySQLdb
from config import * 
from datetime import datetime

conn = False
stype = ""

def filt(item):
    # README:
    # This filter helps to keep only required items in database
    # Result will be saved only if function returns Truthy value
    
    # Here are values You can work with:
    driver = item[0]    # Driver name
    car = item[1]       # Car name
    time = item[2]      # Time in format mm:ss.sss
    platform = item[3]  # Platform (Steam,PS4,Xbox,Oculus)
    flag = item[4]      # Flag id
    founder = item[5]   # Is player founder
    vip = item[6]       # Is player VIP
    stage = item[7]     # Stage number in series
    pid = item[8]       # Player ID (numeric)
    seconds = item[9]   # Time in seconds.ms (ex. 1337.987)

    # build your filter here
    return flag == "40"

def saveResult(stageids, item):
    global conn
    
    if not filt(item):
      return 0
    
    cur = conn.cursor()
    
    driver = item[0]
    car = item[1]
    time = item[2]
    platform = item[3]
    flag = item[4]
    founder = item[5]
    vip = item[6]
    stageidx = item[7]
    pid = item[8]
    seconds = item[9]
    
    ztime = round(seconds * 1000)
    
    try:
        stid = stageids[stageidx]
        if (stid > 1):
            cur.execute("""INSERT INTO results VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(stid,pid,driver,car,str(ztime),flag,founder,vip,platform))
            conn.commit()
            return 1
    except  MySQLdb.Error, e:
        conn.rollback()
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
    return 0


def saveStage(stage):
    global conn
    global stype

    cur = conn.cursor()
    stageids = [];

    for x in stage:
            country = x[0]
            flag = x[1]
            stage = x[2]
            location = x[3]
            daytime = x[4]
            weatherstr = x[5]
            weather = x[6]
            stageidx = str(x[9])
            date = x[8]
            
            location = location.split("/")[-1].split(".")[0]
            if location == "None" : location = "0"
            
            weatherstr = weatherstr.split("/")[-1].split(".")[0]

            flag = flag.split("/")[-1].split(".")[0]
            if flag == "None" : flag = "0"

            try:
	        exists = True
                sql = "SELECT * FROM stages WHERE date='%s' AND type='%s' AND stageidx='%s'" % (date, stype, stageidx)
                cur.execute(sql)
                results = cur.fetchall()
                if (len(results) > 0):
                    print stype + " event on " + date + " has been already imported"
                    stageids.append(-1)
                    exists = True
                else:
		    exists = False
                  
                
                if exists is False:
                    cur.execute("""INSERT INTO stages VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(location, weatherstr, country, flag, stage, daytime, weather, date, stype, stageidx))
                    conn.commit()
                    stageids.append(cur.lastrowid)
            except  MySQLdb.Error, e:
                conn.rollback()
                try:
                    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                except IndexError:
                    print "MySQL Error: %s" % str(e)

    return stageids;

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
                info.append(stageIndex)
                stageInfo.append(info)
                # print "Reading Stage " + str(stageIndex)
            continue
        
        data = line.split(", ")
        if(len(data) < 9):
            continue
        if stageIndex == 0:
            entries += 1

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
            
        # keep only flag id not image path
        flag = data[6].split("/")[-1].split(".")[0]
        if flag == "None" : flag = "0"
        
        founder = "0"
        if data[7]=="True":
	  founder = "1"
        vip = "0"
        if data[8]=="True":
	  vip = "1"
    
            
        #            driver    car      time      plaft   flag  founder  vip    stageid    pid    seconds
        tout.append((data[1], data[3], data[4], platform, flag, founder, vip, stageIndex, data[2], seconds))
        #entries += 1
    return (tout, entries, stageInfo)

def main(argv):
    global conn
    global stype

    if (len(argv) < 2):
        print "Missing arguments."
        print "Usage: python importSql.py date folder"
        sys.exit("")

    conn = MySQLdb.connect(host=db_host,    # your host, usually localhost
                     user=db_user,         # your username
                     passwd=db_passwd,  # your password
                     db=db_database,
                     charset='utf8')        # name of the data base
    
    x = conn.cursor()

    stype = argv[1]

    bfn = "results/" + argv[1] + "/data/" + argv[0] + "_"

    platforms = [["steam","Steam"], ["psn","PS4"], ["live","Xbox"], ["oculus","Oculus"]]

    dfUrl = ""
    hasFiles = False

    for pltf in platforms:   
        dfUrl = os.path.dirname(os.path.abspath(__file__)) + "/" + bfn + pltf[0] + ".txt"
        if (os.path.isfile(dfUrl)):
            hasFiles = True
            break

    if not hasFiles:
        print "Results file not found"
        print "Few things to check:"
        print " - Is date and folder correct?"
        print " - Make sure to run result generator script (daily.py or weekly.py)"
        sys.exit("")

    fileTime = os.path.getmtime(dfUrl)


    dataFile = open(dfUrl, "r")
    dataFileContents = dataFile.read()
    dataFile.close()

    eventInfo = dataFileContents.split("\n")[0].split("\\")

    combined = []
    numEntries = 0

    stageInfo = False

    for pltf in platforms:
        dfUrl = os.path.dirname(os.path.abspath(__file__)) + "/" + bfn + pltf[0] + ".txt"
        if (os.path.isfile(dfUrl)):
            d,e,s2 = getTableData(dfUrl, pltf[1])
            combined.extend(d)
            numEntries += e

            if not stageInfo:
                stageInfo = s2

    stageids = saveStage(stageInfo)
       
    processed = 0
    totali = str(len(combined))
    added = 0
    
    for entry in combined:
        sys.stdout.write("Importing results: " + str(processed) + "/" + totali +"\r")
        sys.stdout.flush()
        added += saveResult(stageids, entry)
        processed += 1
        
    print
    print "Processed " + str(added) + " results"
    conn.close()

if __name__ == "__main__":
   main(sys.argv[1:])