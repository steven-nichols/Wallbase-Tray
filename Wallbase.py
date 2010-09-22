#!/usr/bin/env python

import re, os, os.path
from urllib import urlencode, urlretrieve
from urllib2 import urlopen, Request, URLError
from BeautifulSoup import BeautifulSoup
from time import sleep
import shutil

from Settings import WALLBASE_ALL_SFW, WALLBASE_ANIME_SFW, WALLBASE_GENERAL_SFW
from Settings import WALLBASE_TEMP_FOLDER, WALLBASE_PERMENANT_FOLDER
from DetectOS import DetectOS
from SetWallpaper import SetWallpaper

class Wallbase:

    def __init__(self, url=WALLBASE_ALL_SFW):
        # Search URL
        self.wallbaseurl = url
        
        # Array of links to images on wallbase
        self.imgurls = []
        self.imgurlsIndex = 0
        
        # Array of paths to downloaded images
        self.imgpaths = []
        self.imgpaths.append(self.getCurrentWallpaper())
        self.imgpathsIndex = -1

    def getCurrentWallpaper(self):
        """Returns the path to the current wallpaper image"""
        if DetectOS() == 'gnome':
            return os.popen("gconftool-2 --get /desktop/gnome/background/picture_filename").read().strip()
        elif DetectOS() == 'windows':
            # Wallpaper path stored in "HKEY_CURRENT_USER\Control Panel\Desktop\Wallpaper"
            hKey = _winreg.OpenKey (_winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
            value, type = _winreg.QueryValueEx (hKey, r"Wallpaper")
            _winreg.CloseKey(hKey)
            return value.decode('string_escape')
        else:
            return None

    def setSearchURL(self, url):
        self.wallbaseurl = url
        self.imgurls = []
        self.imgurlsIndex = 0
    
    def getPrevious(self):
        if(self.imgpathsIndex > 0):
            self.imgpathsIndex -= 1
        print self.imgpathsIndex
        prev = self.imgpaths[self.imgpathsIndex]
        SetWallpaper(prev)

    def getNext(self):
        if self.imgpathsIndex >= 0 and self.imgpathsIndex + 1 < len(self.imgpaths):
            self.imgpathsIndex += 1
            next = self.imgpaths[self.imgpathsIndex]
        else:            
            next = self.getNewImage()
            self.imgpaths.append(next)
            self.imgpathsIndex += 1
        SetWallpaper(next)
        print self.imgpaths
    
    def refreshList(self):
        print "Refreshing List..."
        html = self.fetchPage(self.wallbaseurl)
        links = self.parseSearchPage(html)
        for page in links:
            #html = self.fetchPage(page)
            #img = self.parseImagePage(html)
            #self.imgurls.append(img)
            self.imgurls.append(page)
        print "Done. Added %d new images" % len(self.imgurls)
    
    #def getNewImage(self):
    #    print "Fetching image..."
    #    html = self.fetchPage(self.wallbaseurl)
    #    #html = self.fetchPage("http://wallbase.net/search", {'query':'bleach', 'board':'all'})
        
    #    links = self.parseSearchPage(html)
    #    html = self.fetchPage(links[0])
    #    img = self.parseImagePage(html)
    #    self.downloadImage(img, os.path.basename(img))
    #    print "done"
    #    return os.path.abspath(os.path.basename(img))
        
    def getNewImage(self):
        print "Fetching image..."
        if len(self.imgurls) > 0:
            url = self.imgurls.pop(0)
            print url
            img = self.parseImagePage(self.fetchPage(url))
            print img
            path = self.downloadImage(img, os.path.basename(img))
            print "done"
            return path
        else:
            self.refreshList()
            return self.getNewImage()
    
    def fetchPage(self, url, parameters=None):
        ''' Download the page '''
        # GET request
        if parameters is None:
            page = None
            while page is None:
                try:
                    page = urlopen(url)
                except URLError:
                    page = None
                
            return page.readlines()
        # POST request
        else:
            data = urlencode(parameters) # Use urllib to encode the parameters
            request = Request(url, data)
            response = urlopen(request) # This request is sent in HTTP POST
            return response.readlines()
            
    def parseSearchPage(self, html):
        # Parse the search page and return a list of links to image pages
        m = re.findall("http://wallbase.net/wallpaper/\d+", ''.join(html))
        return m
        
    def parseImagePage(self, html):
        soup = BeautifulSoup(''.join(html))
        bigwall = soup.find('div', id='bigwall')
        return bigwall.img['src']
        
    def downloadImage(self, url, filename):
        if not os.path.exists(WALLBASE_TEMP_FOLDER):
            os.makedirs(WALLBASE_TEMP_FOLDER)
        path = os.path.join(WALLBASE_TEMP_FOLDER, filename)
        urlretrieve(url, path)
        return path

    def saveImage(self, path=None):
        if path is None:
            path = os.path.join(os.path.expanduser(WALLBASE_PERMENANT_FOLDER), os.path.basename(self.imgpaths[self.imgpathsIndex]))
        shutil.copyfile(self.imgpaths[self.imgpathsIndex], path)
        print "Saved image as %s" % path

    def cleanUp(self):
        for filename in self.imgpaths[:-1]:
            try:
                print "Deleting %s" % filename
                os.remove(filename)
            except OSError:
                pass
