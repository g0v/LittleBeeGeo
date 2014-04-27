# -*- coding: utf-8 -*-
import json
import urllib2
import requests
import time
import datetime

def toTimestamp(raw):
    tokens = raw.split(',')

def strToDate(rawdate):
    d = datetime.datetime.strptime(rawdate, '%Y/%m/%d')
    return time.mktime(d.timetuple()) + 1e-6 * d.microsecond

def toUnicode(string):
    return unicode(string, 'utf-8', 'ignore')


def parseDocs(lines): # input: line array
#    url = "https://spreadsheets.google.com/pub?key=0Ah-9opsSMy6LdDZBeEdpb0Z2SUlocWE0YVZoU0hmS2c&output=csv"
    result = []
    #url = "https://docs.google.com/spreadsheet/fm?id=t6AxGioFvIIhqa4aVhSHfKg.09543047388341478353.8325993045666016498&fmcmd=5&gid=0"
        
    begin = True
    for line in lines:
        if begin:
            begin = False
            continue
        tokens = line.strip().split(',')
        if tokens:
            time = tokens[0]
            name = tokens[1]
            agenda = tokens[2]
            city = tokens[3]
            road = tokens[4]
            num1 = tokens[5]
            num2 = tokens[6]
            amount = tokens[7]
            rawdate = tokens[8]
            deliver_status = tokens[9]
            note = tokens[10]


        
        #print "road: (%s, %s)" % (repr(road), road.__class__.__name__)
        #print "num1: (%s, %s)" % (repr(num1), num1.__class__.__name__)
        # make address
        name_uni = unicode(name, 'utf-8', 'ignore')
        agenda_uni = unicode(agenda, 'utf-8', 'ignore')
        city_uni = unicode(city, 'utf-8', 'ignore')
        road_uni = unicode(road, 'utf-8', 'ignore')
        num1_uni = unicode(num1, 'utf-8', 'ignore')
        num2_uni = unicode(num2, 'utf-8', 'ignore')
        dt_uni = toUnicode(deliver_status)
        note_uni = toUnicode(note)
        addr1 = city_uni + road_uni + num1_uni + u'路'
        addr2 = city_uni + road_uni + num2_uni + u'路'
        print addr1.encode('utf-8')
        print addr2.encode('utf-8')

        res1 = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % addr1)
        res2 = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % addr2)
        #print res1.content
        print "-----------------------------------------------"
        #print res2.content
        
        j1 = json.loads(res1.content)
        j2 = json.loads(res2.content) 

        lat1 = j1["results"][0]["geometry"]["location"]["lat"]
        lat2 = j2["results"][0]["geometry"]["location"]["lat"]

        lng1 = j1["results"][0]["geometry"]["location"]["lng"]
        lng2 = j2["results"][0]["geometry"]["location"]["lng"]

        print "loc1: %s, %s  loc2: %s, %s" %(lng1, lat1, lng2, lat2)
        geoinfo = { "type": "LineString", 
                    "coordinates": [[lng1, lat1], [lng2, lat2]]}
        item = { "save-time": strToDate(rawdate), 
                "agenda": agenda_uni, 
                "user_name": name_uni, 
                "county":city_uni, 
                "address": road_uni, 
                "start_number": int(num1), 
                "end_number": int(num2), 
                "deliver_time": strToDate(rawdate), 
                "deliver_status": dt_uni, 
                "memo": note_uni, 
                "geo": geoinfo,
                "extension": {}}
        result.append(item)
    
    with open("deliverData.json", "w") as fd_out:
        json.dump(result, fd_out)
        fd_out.close()

if __name__ == '__main__':
    with open('ccc2.csv', "r") as fd:
        lines = fd.readlines()
        parseDocs(lines)


