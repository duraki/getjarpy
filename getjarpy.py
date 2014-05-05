__author__  = 'dn5'
__blog__    = 'http://dn5.ljuska.org'
__github__  = 'https://github.com/dn5/getjarpy'
__twitter__ = 'https://twitter.com/dn5__'
__email__   = 'dn5@dn5.ljuska.org'

import BeautifulSoup
import urllib2
import socket
import re
import sys

########################## Details setting / About
gjpyLogo = "            _    _                        \n"\
           "  __ _  ___| |_ (_) __ _ _ __ _ __  _   _ \n"\
           " / _` |/ _ \ __|| |/ _` | '__| '_ \| | | |\n"\
           "| (_| |  __/ |_ | | (_| | |  | |_) | |_| |\n"\
           " \__, |\___|\__|/ |\__,_|_|  | .__/ \__, |\n"\
           " |___/        |__/           |_|    |___/ \n"\
           "Simple GetJar java application downloader   "\

gjpyInfo = "Coded by dn5 / http://dn5.ljuska.org / @dn5__ \n"

gjpyUsage = "Usage: python getjarpy.py http://getjar.mobi/mobile/xxxxxx/name-of-app-model localFileName"
gjpyExample = "Example: python getjarpy.py http://www.getjar.mobi/mobile/567704/fooddash-for-nokia-5130-xpressmusic/ FoodDash"

########################## Basic testing for arguments
if len(sys.argv) == 1:
    print gjpyLogo
    print gjpyInfo
    print "You didn't supply arguments! Use getjar.py --help for details."
    sys.exit()

if len(sys.argv) == 2:
    if sys.argv[1] == "--help":
        print gjpyLogo
        print gjpyInfo
        print gjpyUsage
        print gjpyExample
        sys.exit()

if len(sys.argv) == 3:
    print gjpyLogo
    print gjpyInfo
    print gjpyUsage
    print gjpyExample

    print "\nSetting a link for exploitation!"
    permaLink = sys.argv[1]
    print permaLink +"\n"

    #print "\nYour settings:"
    #print "Argument 0: " + sys.argv[0]
    #print "Argument 1: " + sys.argv[1]
    #print "Argument 2: " + sys.argv[2]

    print "\nWriting other settings!"

    ########################## Setting variables
    ua = "Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (J2ME/22.478; U; en) Presto/2.5.25 Version/10.54" # User-agent
    ol = "http://m.getjar.mobi/" # Original link

    mobileModel = "nokia-5130-xpressmusic/"
    setJavaModel = "--java/?d=-java"
    localFile = sys.argv[2]+".jar"

    ########################## Setting particular exploitation constants
    mainLink = permaLink.replace("-for-"+mobileModel, "-for"+setJavaModel)
    mainLink = mainLink.replace("http://www.", "http://m.")
    print "Trying to exploit this URL: " + mainLink

    ########################## Starting the production
    req = urllib2.Request(mainLink)
    req.add_unredirected_header('User-Agent', ua)
    response = urllib2.urlopen(req)

    #print req.header_items()

    try:
        html = response.read()
        # print html
    except urllib2.URLError, e:
        print "w00t w00t - Error while reading data. Are you connected to the interwebz?!", e
        sys.exit()

    print "Extracting some files from URL ..."
    soup = BeautifulSoup.BeautifulSoup(html)
    form = soup.find('form', id='form_product_page').get('action')

    reqDownload = urllib2.Request(ol + form)
    responseDownload = urllib2.urlopen(reqDownload)
    responseRead = responseDownload.read()

    print "Getting file data and extracting installation!"
    print #responseRead

    pLink = re.search("(?P<url>http?://[^\s]+)", responseRead).group("url") # Extracting URL from "responseRead"

    print "Getting a JAR file for the last time, I promise."
    jarFile = urllib2.urlopen(pLink)
    print "Opening a file for testing, just to make sure everything works!"
    output = open(localFile,'wb')
    print "Writting data ..."
    output.write(jarFile.read())
    output.close()
    print "w00t w00t, your file is ready to be transfered or reverse engineered! Filename: " + localFile