import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
import unidecode

class Scrapping:
    def __init__(self):
        self.baseurl  = 'https://www.mtgtop8.com/event'
        self.scryfall = 'https://api.scryfall.com/cards'

    # tournament url
    def getEventUrl(self, url):
        return self.baseurl + '?e=' + url + '&f=LE'

    # get soup
    def getSoup(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        return soup
    
    # get soup on json format
    def getJsonSoup(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        data = json.loads(soup.text.encode('utf-8'))

        return data
    
    # player deck url
    def getPlayerDeckUrl(self, url):
        return self.baseurl + url
    
    # card scryfall url
    def getScryfallUrlCardData(self, name):
        return self.scryfall + '/named?exact=' + name
    
    # extrange names
    def convertCardName(self, cardName):
        cardName = unidecode.unidecode(cardName)
        cardName = cardName.replace('L 3/4rien', 'Lorien')
        cardName = cardName.replace('Lurien', 'Lorien')
        cardName = cardName.replace('LUrien', 'Lorien')
        cardName = cardName.replace('dZm', 'dum')
        cardName = cardName.replace(' ', '%20')
        cardName = cardName.replace(',', '')
        cardName = cardName.replace('&', '')

        return cardName
