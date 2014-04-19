# -*- coding: utf-8 -*-
import json
import urllib2
import requests

def outputResult(outfile):
    ofd = open(outfile, 'w')
    c = 0
    ofd.write("[")
    for k, comp in companys.iteritems():
        if c == 0: ofd.write(", \n")
        ofd.write("%s" % json.dumps(comp, ensure_ascii=False, encoding='utf-8'))
        c += 1
    ofd.write("]")
    ofd.close()

def parseDocs():
#    url = "https://spreadsheets.google.com/pub?key=0Ah-9opsSMy6LdDZBeEdpb0Z2SUlocWE0YVZoU0hmS2c&output=csv"
    
    url = "https://docs.google.com/spreadsheet/fm?id=t6AxGioFvIIhqa4aVhSHfKg.09543047388341478353.8325993045666016498&fmcmd=5&gid=0"
    '''
    values = {  'encodeURIComponent': '1',
                'step': '1',
                'firstin': '1',
                'off':'1',
                'TYPEK':target }
    '''
    #data = {}
    #req_data = urllib.urlencode(data)
    #res = requests.get(url)    
    #print res.content
    with open('ccc.csv', "r") as fd:
        lines = fd.readlines()
        begin = True
        for line in lines:
            if begin:
                begin = False
                continue
            tokens = line.strip().split(',')
            road = tokens[2]
            num1 = tokens[3]
            num2 = tokens[4]
            
            print "road: (%s, %s)" % (repr(road), road.__class__.__name__)
            print "num1: (%s, %s)" % (repr(num1), num1.__class__.__name__)

            road_uni = unicode(road, 'utf-8', 'ignore')
            num1_uni = unicode(num1, 'utf-8', 'ignore')
            num2_uni = unicode(num2, 'utf-8', 'ignore')
            addr1 = road_uni + num1_uni + u'路'
            addr2 = road_uni + num2_uni + u'路'
            #addr1 = urllib2.quote(addr1.encode('utf-8'))
            #addr2 = urllib2.quote(addr2.encode('utf-8'))
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

if __name__ == '__main__':
    #parseDirectors('sii')
    parseDocs()


