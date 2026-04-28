from functions.scrapping import Scrapping
from classes.top8 import Top8
from classes.player import Player
from classes.card import Card

class MtgTop8:
    def __init__(self, idTournament):
        self.baseurl      = 'https://www.mtgtop8.com/event'
        self.id           = None
        self.idTournament = idTournament
        self.players      = []
        self.cards        = []

    def getCards(self):
        return self.cards
    
    def setPlayers(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players

    # tournament url
    def getEventUrl(self, url):
        return self.baseurl + '?e=' + url + '&f=LE'
    
    # player deck url
    def getPlayerDeckUrl(self, url):
        return self.baseurl + url
    
    def getSoupData(self):
        soup     = Scrapping()
        soupData = soup.getSoup(self.getEventUrl(self.idTournament))
        
        return soupData
    
    # get data tournament from website - scrap mtgtop8
    def getTournamentData(self, tournament, soup):
        for tournamentSoup in soup.findAll('div', attrs={"class": 'S14'}):
            num = 0
            for tournamentDivs in tournamentSoup.findAll('div'):
                if num == 1:
                    if tournamentDivs.text is not None:
                        text        = tournamentDivs.text
                        textSplit   = text.split(' - ')
                        textDate    = textSplit[1]
                        textPlayers = textSplit[0].replace('players', '')
                    break
                num += 1
            break

        # set extra tournament data
        tournament.setDate(textDate)
        tournament.setNumPlayers(textPlayers)
        if not tournament.setTournamentIdFromDB():
            tournament.saveTournament()

    # save players and decks on db
    def setTop8PlayersAndDecks(self, soup, id):
        self.setTop8Players(soup)
        top8 = Top8(id)
        top8.savePlayers(self.getPlayers())
        top8.setTop8PlayersDecks(self.getPlayers(), False)

    # get players info and save on database
    def setTop8Players(self, soup):
        self.scrapTopPlayers(soup, "chosen_tr")
        self.scrapTopPlayers(soup, "hover_tr")

    # scrap players
    def scrapTopPlayers(self, soup, className):
        for set in soup.findAll('div', attrs={"class": className}):
            num = 0

            for link in set.find_all('a'):

                if link.text != '':
                    if num == 0:
                        deckName = link.text
                        deckHref = link.get('href')
                    if num == 1:
                        playerName = self.getPlayerName(link, soup)

                    num+=1

            if playerName != '' and deckHref != '' and deckName != '':
                self.setTopPlayer(playerName, deckHref, deckName, self.id)
                deckName   = ''
                playerName = ''

    def setTopPlayer(self, playerName, deckHref, deckName, idTournament):        
        deckUrl = self.getPlayerDeckUrl(deckHref)
        num     = len(self.players)
        player  = Player(num+1, playerName, deckUrl, idTournament, deckName)

        self.setPlayers(player)

    def getPlayerName(self, link, soup):
        playerName = link.text
        
        # print("%s - %s" %(playerName, soup.original_encoding))
        if (soup.original_encoding == 'cp850'):
            name = playerName.encode('cp850')
            playerName = name.decode(encoding="ISO-8859-1", errors="ignore")

        if(soup.original_encoding == "windows-1250"):
            name = playerName.encode('windows-1250')
            playerName = name.decode(encoding="ISO-8859-1", errors="ignore")

        return playerName
