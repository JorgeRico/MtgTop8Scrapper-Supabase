from classes.mtgTop8 import MtgTop8
from classes.player import Player
from classes.deck import Deck

class Top8:
    def __init__(self, idTournament):
        self.idTournament = idTournament
        self.topPlayers   = []

    # get list of players
    def getTopPlayers(self):
        return self.topPlayers
    
    def setTopPlayers(self, player):
        self.topPlayers.append(player)
    
    # save players on list
    def setTopPlayer(self, playerName, deckHref, deckName):
        mtgtop8 = MtgTop8()
        
        deckUrl = mtgtop8.getPlayerDeckUrl(deckHref)
        num     = len(self.topPlayers)
        player  = Player(num+1, playerName, deckUrl, self.idTournament, deckName)
        self.setTopPlayers(player)

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
                self.setTopPlayer(playerName, deckHref, deckName)
                deckName   = ''
                playerName = ''

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
    
    # get players info and save on database
    def setTop8Players(self, soup):
        self.scrapTopPlayers(soup, "chosen_tr")
        self.scrapTopPlayers(soup, "hover_tr")

    # save players on db
    def savePlayers(self):
        print('       * Players:')
        for item in self.topPlayers:
            idPlayer = item.existsPlayerOnDB()
            
            if idPlayer is None:
                add = True
            elif (len(idPlayer) == 0):
                add = True
            else:
                add = False
                if idPlayer[0].get('idDeck') is not None:
                    item.setPlayerIdDeck(idPlayer[0].get('idDeck'))
                
            if add == True:
                self.saveItemPlayer(item)
            else:
                self.existItemPlayer(item, idPlayer)
            
    def saveItemPlayer(self, item):
        print('         - Player saved on DB: %s - %s' %(item.getPlayerNum(), item.getPlayerName()))
        idPlayerInserted = item.savePlayer(self.idTournament)
        
        deck = Deck()
        item.setIdPlayer(idPlayerInserted.data[0].get('id'))
        deck.savePlayerDeck(item, idPlayerInserted.data[0].get('id'))

    def existItemPlayer(self, item, idPlayer):
        print('         - Players is on DB: %s - %s' %(item.getPlayerNum(), item.getPlayerName()))
        item.setIdPlayer(idPlayer[0].get('id'))

    # top8 decks saved
    def setTop8PlayersDecks(self):
        print('       * Decks:')

        deck = Deck()
        for item in self.topPlayers:
            if item.idDeck is None:
                deck.savePlayerDeck(item, item.idPlayer)

            result = deck.playerHasIdDeckOnDB(item.idPlayer)
            self.setLoadCards(result, item)
            
    # check if deck has cards loaded, if not load cards and update deck on db
    def setLoadCards(self, result, item):
        if result[0].get('decks').get('cardsLoaded') == False:
            deck = Deck()
            deck.setDeck(result[0].get('idDeck'), item.deckHref, item.idPlayer)
            print('         - Deck saved on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
        else:
            print('         - Deck is on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))

    # save players and decks on db
    def setTop8PlayersAndDecks(self, soup):
        self.setTop8Players(soup)
        self.savePlayers()
        self.setTop8PlayersDecks()