from classes.deck import Deck
from functions.helpers import Helpers

class Top8:
    def __init__(self):
        self.topPlayers = []

    # get list of players
    def getTopPlayers(self):
        return self.topPlayers
    
    def setTopPlayers(self, players):
        self.topPlayers = players

    # save players on db
    def savePlayers(self, players):
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
        print(Helpers.GREEN + '         - Player saved on DB: %s | %s' %(item.getPlayerNum(), item.getPlayerName()) + Helpers.RESET)
        idPlayerInserted = item.savePlayer(item.getIdTournament())
        
        item.setIdPlayer(idPlayerInserted.data[0].get('id'))

    def existItemPlayer(self, item, idPlayer):
        print(Helpers.ORANGE + '         - Player is on DB: %s | %s' %(item.getPlayerNum(), item.getPlayerName()) + Helpers.RESET)

        item.setIdPlayer(idPlayer[0].get('id'))

    # top8 id decks saved if is None
    def setTop8PlayersIdDecks(self, topPlayers):
        deck = Deck()
        for item in topPlayers:    
            if item.idDeck is None:
                deck.savePlayerDeck(item, item.idPlayer)
