# -*- encoding: utf-8 -*-

'''
    @author Lucas Deutschland
'''
from bs4 import BeautifulSoup
import requests
import re
import urllib2

try:
    def search(search, sites, datei):
        seiten = sites               
        site = "http://www.google.com/search?q=%s&start=%i"%(search,seiten)
        page = requests.get(site)
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
        print search1
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
        if any(t in page.text for t in output):
            outF = open(decodedUrl, "w")
            outF.write("\n %s"%decodedUrl)
            outF.close()
            print ("Site is vulnerable(%s)"%decodedUrl)
        else:
            print ("Site isn't vulnerable(%s)"%decodedUrl)



    def start_menu():
        begriff = raw_input("Google Dork: ")
        seiten = raw_input("How many sites do you want to open?(Recommended: 8): ")
        google_search(begriff, seiten)
        

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





