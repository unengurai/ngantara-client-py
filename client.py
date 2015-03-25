#!/usr/bin/python
import sys
import os
import json
import urllib2
import urllib
import base64
from time import sleep

#iniPath = os.getcwd()
sys.path.append(os.getcwd())
import websearch

##- SET SERVER IP/ADDRESS
server_addr = 'http://127.0.0.1:6969'

ws0 = websearch.websearch()
ws1 = websearch.websearch()

def gSearch(kw, kwid):
    ws0.keyword = kw
    ws0.stop = 200
    surl = server_addr + '/sr/'
    for url in ws0.google():
        smesg = {'url': url, 'kwid': kwid}
        resp(surl, smesg)
        print "gsearch:-- " + url
        #exit()


def otherSearch(kw):
    ws1.keyword = kw
    for url in ws1.yahoobing():
        resp(url, smesg)
        print "osearch:-- " + url
        #magentoCek(url, kw)


def getkw(saddr):
    req = urllib2.Request(saddr)
    response = urllib2.urlopen(req)
    mesg = response.read()
    return json.loads(mesg)


def resp(saddr, smesg):
    smesg = json.dumps(smesg)
    smesg = {'data': base64.b64encode(str(smesg))}
    headers = {'User-Agent': 'tukang ngantara 0.1'}
    data = urllib.urlencode(smesg)
    print saddr + " \n--smesg: "+ str(smesg)
    print headers
    req = urllib2.Request(saddr, data, headers)
    respon = urllib2.urlopen(req)

    respon_text = respon.read()
    print "respon : " + respon_text
    json_text = json.loads(str(respon_text))
    #print json_text
    return json_text


if __name__ == '__main__':
    while True:
        data = {'kw': None,
                'kwid': None}
        surl = server_addr + '/gk/'
        data = getkw(surl)
        print(data)
        #exit()
        if data['kw'] is not None:
            smesg = {'act': 'OK', 'kwid': data['kwid']}
            resp(surl, smesg)
            #otherSearch(kw)
            gSearch(data['kw'], data['kwid'])
            smesg = {'act': 'DONE', 'kwid': data['kwid']}
            resp(surl, smesg)
            sleep(120)
        else:
            sleep(3600)
