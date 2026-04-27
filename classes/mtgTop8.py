class MtgTop8:
    def __init__(self):
        self.baseurl  = 'https://www.mtgtop8.com/event'

    # tournament url
    def getEventUrl(self, url):
        return self.baseurl + '?e=' + url + '&f=LE'
    
    # player deck url
    def getPlayerDeckUrl(self, url):
        return self.baseurl + url