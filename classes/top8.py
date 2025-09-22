from functions.functions import Scrapping
from classes.player import Player
from classes.deck import Deck
from functions.db import Db
from data.tableNames import playerTable

class Top8:
    def __init__(self):
        self.topPlayers = []

    # get list of players
    def getTopPlayers(self):
        return self.topPlayers
    
    # save players on list
    def setTopPlayer(self, playerName, deckHref, deckName, idTournament):
        scrapping = Scrapping()
        if playerName != '' and deckHref != '':
            num    = len(self.topPlayers)
            player = Player(num+1, playerName, scrapping.getPlayerDeckUrl(deckHref), idTournament, deckName)
            self.topPlayers.append(player)
            
            return True
        
        return False

    # scrap players
    def scrapTopPlayers(self, soup, className, idTournament):
        for set in soup.findAll('div', attrs={"class": className}):
            num = 0

            for link in set.find_all('a'):

                if link.text != '':
                    if num == 0:
                        deckName = link.text
                        deckHref = link.get('href')

                    if num == 1:
                        playerName = link.text
                        # print("%s - %s" %(playerName, soup.original_encoding))
                        if (soup.original_encoding == 'cp850'):
                            name = playerName.encode('cp850')
                            playerName = name.decode(encoding="ISO-8859-1",errors="ignore")
                        if(soup.original_encoding == "windows-1250"):
                            name = playerName.encode('windows-1250')
                            playerName = name.decode(encoding="ISO-8859-1",errors="ignore")
                    num+=1
            if self.setTopPlayer(playerName, deckHref, deckName, idTournament) == True:
                deckName   = ''
                playerName = ''
    
    # get players info and save on database
    def setTop8Players(self, soup, idTournament):
        self.scrapTopPlayers(soup, "chosen_tr", idTournament)
        self.scrapTopPlayers(soup, "hover_tr", idTournament)
        self.savePlayers()

    # save deck
    def saveDeck(self, item, idPlayer):
        deck = Deck()
        response = deck.saveDeck(item.getPlayerDeckName())
        item.savePlayerIdDeck(response[0].get('id'), idPlayer)

    # save players on db
    def savePlayers(self):
        print('       * Players:')
        for item in self.topPlayers:
            idPlayer = item.existsPlayerOnDB()
            
            try:
                if (len(idPlayer) == 0):
                    print('         - Player saved on DB: %s - %s' %(item.getPlayerNum(),item.getPlayerName()))
                    idPlayerInserted = item.savePlayer()
                    self.saveDeck(item, idPlayerInserted[0].get('id'))
                else:
                    print('         - Players is on DB: %s - %s' %(item.getPlayerNum(),item.getPlayerName()))
            except Exception:
                if (idPlayer is None):
                    print('         - Player saved on DB: %s - %s' %(item.getPlayerNum(),item.getPlayerName()))
                    idPlayerInserted = item.savePlayer()
                    self.saveDeck(item, idPlayerInserted[0].get('id'))
                else:
                    print('         - Players is on DB: %s - %s' %(item.getPlayerNum(),item.getPlayerName()))

    # top8 decks saved
    def setTop8PlayersDecks(self, idTournament):
        response = self.getTop8PlayersFromDb(idTournament)
        print('       * Decks:')
        for item in response:
            if item.get('decks').get('cardsLoaded') == False:
                deck = Deck()
                # delete previous results before upload all deck
                deck.deleteDeckCards(item.get('idDeck'))
                # scrap deck
                soup = Scrapping()
                soup = soup.getSoup(item.get('deckHref'))
                
                deck.getDeck(item.get('idDeck'), soup)
                deck.updateCardsLoaded(item.get('idDeck'))
                print('         - Deck saved on DB: %s - %s' %(item.get('decks').get('name'), item.get('name')))
            else:
                print('         - Deck is on DB: %s - %s' %(item.get('decks').get('name'), item.get('name')))

    # get players from DB
    def getTop8PlayersFromDb(self, idTournament):
        db       = Db()
        response = db.getTableDataQueryWhere(playerTable, 'id, name, idDeck, deckHref, decks(cardsLoaded, name)', 'idTournament', idTournament)

        return response
    
    # check if player has deck on db
    def playerHasIdDeckOnDB(self, idPlayer):
        db       = Db()
        response = db.getTableDataQueryWhere(playerTable, 'idDeck', 'id', idPlayer)

        return response