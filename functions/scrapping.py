import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
import urllib3
import time

class Scrapping:
    def __init__(self):
        self.headers  = { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' }

    # get soup
    def getSoup(self, url):
        try:
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except Exception as error:
            print(error)
    
    # get soup on json format
    # for scryfall api
    def getJsonSoup(self, url):
        # bypass to scryfall block
        time.sleep(1)
        page = urllib3.request("GET", url, headers=self.headers)
        soup = BeautifulSoup(page.data, 'html.parser')
        data = json.loads(soup.text.encode('utf-8'))

        return data
 