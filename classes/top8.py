from classes.deck import Deck

class Top8:
    def __init__(self, idTournament):
        self.idTournament = idTournament
        self.topPlayers   = []

    # get list of players
    def getTopPlayers(self):
        return self.topPlayers
    
    def setTopPlayers(self, players):
        self.topPlayers = players

    # save players on db
    def savePlayers(self, players):
        print('       * Players:')
        for item in players:
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
    def setTop8PlayersDecks(self, topPlayers, isMtgDecks=None):
        print('       * Decks:')

        deck = Deck()
        for item in topPlayers:            
            if item.idDeck is None:
                deck.savePlayerDeck(item, item.idPlayer)
            result = deck.playerHasIdDeckOnDB(item.idPlayer)
            self.setLoadCards(result, item, isMtgDecks)
            
    # check if deck has cards loaded, if not load cards and update deck on db
    def setLoadCards(self, result, item, isMtgDecks = False):
        if result[0].get('decks').get('cardsLoaded') == False:
            if not isMtgDecks:
                deck = Deck()
                deck.setDeck(result[0].get('idDeck'), item.deckHref, item.idPlayer, isMtgDecks)
            print('         - Deck saved on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
        else:
            print('         - Deck is on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))

    def saveTop8Data(self, players):
        self.savePlayers(players)
