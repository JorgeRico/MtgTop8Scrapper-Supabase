from classes.db import Db
from data.tableNames import deckTable, cardsTable, playerTable

class Deck:
    def __init__(self):
        self.db = Db()

    # set deck on database
    def setDeck(self, idDeck, cards, idPlayer):
        # delete previous results before upload all deck
        self.deleteDeckCards(idDeck)

        self.saveDeckCardsList(cards)
        self.updateCardsLoaded(idDeck)
        self.updateDeckPlayer(idDeck, idPlayer)

    # save deck name
    def saveDeck(self, name):
        item     = { "name" : name }
        response = self.db.insert(deckTable, item)

        return response.data

    # save deck list on DB
    def saveDeckCardsList(self, cards):
        for card in cards:
            self.db.insert(cardsTable, card.getCardItem())

    # save player idDeck on DB
    def updateCardsLoaded(self, idDeck):
        self.db.update(deckTable, {'cardsLoaded': True}, 'id', idDeck)

    # save player on DB
    def updateDeckPlayer(self, idDeck, idPlayer):
        self.db.update(deckTable, {'idPlayer': idPlayer}, 'id', idDeck)

    # save player idDeck on DB
    def deleteDeckCards(self, idDeck):
        self.db.delete(cardsTable, 'idDeck', idDeck)

    # save player deck
    def savePlayerDeck(self, item, idPlayer):
        response = self.saveDeck(item.getPlayerDeckName())
        item.savePlayerIdDeck(response[0].get('id'), idPlayer)

    # check if player has deck on db
    def playerHasIdDeckOnDB(self, idPlayer):
        response = self.db.getTableDataQueryWhere(playerTable, 'id, name, idDeck, decks(cardsLoaded, name)', 'id', idPlayer)

        return response