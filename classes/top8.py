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
        if playerName != '' and deckHref != '' and deckName != '' and idTournament != '':
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
        deck     = Deck()
        response = deck.saveDeck(item.getPlayerDeckName())
        item.savePlayerIdDeck(response[0].get('id'), idPlayer)

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
        print('         - Player saved on DB: %s - %s' %(item.getPlayerNum(),item.getPlayerName()))
        idPlayerInserted = item.savePlayer()
        try:
            item.setIdPlayer(idPlayerInserted[0].get('id'))
            self.saveDeck(item, idPlayerInserted[0].get('id'))
        except Exception:
            idPlayerInserted = item.savePlayer()
            item.setIdPlayer(idPlayerInserted[0].get('id'))
            self.saveDeck(item, idPlayerInserted[0].get('id'))


    def existItemPlayer(self, item, idPlayer):
        print('         - Players is on DB: %s - %s' %(item.getPlayerNum(),item.getPlayerName()))
        item.setIdPlayer(idPlayer[0].get('id'))

    # top8 decks saved
    def setTop8PlayersDecks(self):
        print('       * Decks:')
        for item in self.topPlayers:
            if item.idDeck is None:
                self.saveDeck(item, item.idPlayer)

            result = self.playerHasIdDeckOnDB(item.idPlayer)
            
            if result[0].get('decks').get('cardsLoaded') == False:
                deck = Deck()
                # delete previous results before upload all deck
                deck.deleteDeckCards(result[0].get('idDeck'))
                # scrap deck
                soup = Scrapping()
                soup = soup.getSoup(item.deckHref)
                
                deck.getDeck(result[0].get('idDeck'), soup)
                deck.updateCardsLoaded(result[0].get('idDeck'))
                deck.updateDeckPlayer(result[0].get('idDeck'), item.idPlayer)
                
                print('         - Deck saved on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
            else:
                print('         - Deck is on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
    
    # check if player has deck on db
    def playerHasIdDeckOnDB(self, idPlayer):
        db       = Db()
        response = db.getTableDataQueryWhere(playerTable, 'id, name, idDeck, decks(cardsLoaded, name)', 'id', idPlayer)

        return response