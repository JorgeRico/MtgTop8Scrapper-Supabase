import urllib
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import urllib3
import time

class Scrapping:
    def __init__(self):
        self.headers = { 
            "User-Agent"      : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language" : "en-US,en;q=0.5",
            "Referer"         : "https://www.google.com/"
        }

    # get soup
    def getSoup(self, url):
        try:
            page = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(page) as response:
                html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        except urllib.error.HTTPError as e:
            print("Status:", e.code)
    
    # get soup on json format
    # for scryfall api
    def getJsonSoup(self, url):
        # bypass to scryfall block
        time.sleep(1)
        page = urllib3.request("GET", url, headers=self.headers)
        soup = BeautifulSoup(page.data, 'html.parser')
        data = json.loads(soup.text.encode('utf-8'))

        return data
 