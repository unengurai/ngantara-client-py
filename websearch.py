#!/usr/bin/python
# Cari pakek Google search engine.
# hasil yang di tampilkan berupa domain unik(hanya 1 domain), bukan link yank unik
#

import urllib2
import random
import os
import time
from urllib import quote_plus
from urllib2 import Request, urlopen
from cookielib import LWPCookieJar
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qs


class websearch:
    url = ''
    keyword = ''
    lang='en'
    num=10
    pause=15
    start=0
    stop=None
    tld='com'

    domFilter = ("flickr.com", "yahoo", "webcache", "youtube.com", "facebook.com", 
                "twitter.com", "pinterest.com", "blogspot.com", "wordpress.com", "tumblr.com", "github.com",
                "stackoverflow.com", "srpcache", ".metacafe.com", "google.com", "linkedin.com", "microsoft.com", "bing.com",
                "wikipedia.org", "sourceforge.net", "quora.com", "wordpress.org"
                )

    def getpage(self,url):
        header = ['Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; WOW64; Trident/5.0',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.2; es-US ) AppleWebKit/540.0 (KHTML like Gecko) Version/6.0 Safari/8900.00',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0"',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.26.17 (KHTML like Gecko) Version/6.0.2 Safari/536.26.17'
        ]
            
        cookie_jar = LWPCookieJar('/tmp/.gc')
        try:
            cookie_jar.load()
        except Exception, e:
            pass
        html = ''
        try:
            request = Request(url)
            agent = random.choice(header)
            request.add_header('User-Agent', agent )
            cookie_jar.add_cookie_header(request)
            response = urlopen(request)
            cookie_jar.extract_cookies(response, request)
            html = response.read()
            response.close()
            cookie_jar.save()
        except:
            pass
        return html

    def gfilter(self, link):
        o = urlparse(link, 'http')
        try:
            if o.netloc and 'google' not in o.netloc:
                return link

            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]

                o = urlparse(link, 'http')
                if o.netloc and 'google' not in o.netloc:
                    return link

        except Exception, e:
            #print "[+]Error: "+str(e)
            pass
        return None

    def google(self):
        """

        :rtype : object
        """

        print "gsearch started.................................................."  #########################################################################################

        googleTld = ["com","ae","com.af","com.ag","off.ai","am","com.ar","as","at","com.au","az","ba","com.bd","be","bg","bi","com.bo","com.br","bs","co.bw","com.bz","ca","cd","cg","ch","ci","co.ck","cl","com.co","co.cr","com.cu","de","dj","dk","dm","com.do","com.ec","es","com.et","fi","com.fj","fm","fr","gg","com.gi","gl","gm","gr","com.gt","com.hk","hn","hr","co.hu","co.id","ie","co.il","co.im","co.in","is","it","co.je","com.jm","jo","co.jp","co.ke","kg","co.kr","kz","li","lk","co.ls","lt","lu","lv","com.ly","mn","ms","com.mt","mu","mw","com.mx","com.my","com.na","com.nf","com.ni","nl","no","com.np","nr","nu","co.nz","com.om","com.pa","com.pe","com.ph","com.pk","pl","pn","com.pr","pt","com.py","ro","ru","rw","com.sa","com.sb","sc","se","com.sg","sh","sk","sn","sm","com.sv","co.th","com.tj","tm","to","tp","com.tr","tt","com.tw","com.ua","co.ug","co.uk","com.uy","uz","com.vc","co.ve","vg","co.vi","com.vn","vu","ws","co.za","co.zm"]
        
        lang = self.lang
        num = self.num
        pause = self.pause
        start = self.start
        stop  = self.stop
        gtld = self.tld

        url_home          = "http://www.google.%(tld)s/"
        url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
        url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
        url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
        url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"
    
        domList = []
        usingTld = []
        query = quote_plus(self.keyword)
        
        if 'all' in gtld:
            usingTld=googleTld
        else:
            usingTld.append(gtld)

        print "KW : " + str(self.keyword)  #########################################################################################

        for tld in usingTld:
            try:
                url = url_home % vars()
                self.getpage(url) #<--ambil cookie google duluw
                if start:
                    if num == 10:
                        url = url_next_page % vars()
                    else:
                        url = url_next_page_num % vars()
                else:
                    if num == 10:
                        url = url_search % vars()
                    else:
                        url = url_search_num % vars()
                
                while not stop or start < stop:
                    #pausetime = random.randint(1,11) * self.pause
                    pausetime = random.randint(1,11) * 3

                    print "SLEEP " + str(pausetime)  #########################################################################################

                    time.sleep(pausetime)

                    print "GET: " + str(url)  #########################################################################################

                    html = self.getpage(url)
                    soup = BeautifulSoup(html)

                    print soup.title.string  #########################################################################################

                    try:
                        anchors = soup.find('div', id="search").findAll('a')
                        for a in anchors:

                            try:
                                link = a['href']
                            except KeyError:
                                continue

                            link = self.gfilter(link)
                            if not link:
                                continue
                                
                            if not (any (sf in a['href'] for sf in self.domFilter)):
                                t2host = link.split("/",3)
                                linkDomain = t2host[2]
                                if linkDomain not in domList:
                                    domList.append(linkDomain)
                                    yield link
                                
                    except Exception, e:
                        #print "[+]Error: "+str(e)
                        pass

                    if not soup.find(id="nav"):
                        break

                    start += num
                    if num == 10:
                        url = url_next_page % vars()
                    else:
                        url = url_next_page_num % vars()
            except Exception, e:
                #print "[+]Error: "+str(e)+"\n WHEN GET: "+url_home
                pass

## OTHER SEARCH ENGINE..
    def yahoobing(self):
        kw = quote_plus(self.keyword)
        ydoms =  ("ca.","de.","es.","fr.","it.","uk.","at.","au.","hk.","ar.","ch.","co.","dk.","fi.","gr.","ie.","in.","jp.","kr.","my.","pl.","ro.","ru.","se.","ve.","")
        domList = []
        for dom in ydoms:
            yb = 1
            ysearch = True
            while ysearch:
                yburl = yb
                yurl = "http://"+dom+"search.yahoo.com/search?n=100&p="+kw+"&b="+str(yburl)
                #print "==== "+yurl
                countUrl =0
                try:
                    html = self.getpage(yurl)
                    soup = BeautifulSoup(html)
                    anchors = soup.findAll('a')
                    
                    for a in anchors:
                        if '%3a' in a['href']:
                            if not (any (s in a['href'] for s in self.domFilter)):
                                countUrl += 1
                                link = a['href'].split('%3a//')[1]
                                t2host = link.split("/",3)
                                linkDomain = t2host[0]
                                if linkDomain not in domList:
                                    domList.append(linkDomain)
                                    yield link
                except:
                    pass
                                
                if countUrl == 0:
                    ysearch = False
                    
                pausetime = random.randint(1,11) * 2
                time.sleep(pausetime)
                yb += 100
                
        ##-- bing search engine
        bi = 1
        bsearch = True
        while bsearch:
            bfirst = str(bi)
            burl = "http://www.bing.com/search?q="+kw+"&form=PERE&filt=all&first="+bfirst
            #print "==== "+burl
            countUrl =0
            try:
                html = self.getpage(burl)
                soup = BeautifulSoup(html)
                anchors = soup.findAll('a')
                
                for a in anchors:
                    #print a
                    link = a['href']
                    if (link.startswith('http')) and not (any (s in link for s in self.domFilter)):
                        countUrl += 1
                        t2host = link.split("/",3)
                        linkDomain = t2host[2]
                        if linkDomain not in domList:
                            domList.append(linkDomain)
                            yield link
            except:
                pass

            if countUrl == 0:
                bsearch = False
                
            pausetime = random.randint(1,12) * 2
            time.sleep(pausetime)
            bi += 10

    def printSeting(self):
        print self.url
        print self.keyword
        print self.lang
        print self.num
        print self.pause
        print self.start
        print self.stop
        print self.tld
