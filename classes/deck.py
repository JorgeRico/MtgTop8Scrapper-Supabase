from classes.card import Card
from classes.db import Db
from data.tableNames import deckTable, cardsTable, playerTable
from functions.scrapping import Scrapping

class Deck:
    def __init__(self):
        self.cards = []
        self.db    = Db()

    # get list of cards on deck
    def getDeckCards(self):
        return self.cards
    
    def setCards(self, card):
        self.cards.append(card)

    # scrap deck info
    def getDeck(self, idDeck, deckHref):
        soup = Scrapping()
        soup = soup.getSoup(deckHref)

        for cards in soup.findAll('div', attrs={"class": 'deck_line hover_tr'}):
            board = cards.get('id')[:2]

            if cards.text[1] == ' ':
                num  = cards.text[0]
                name = cards.text[2:].strip()
            if cards.text[2] == ' ':
                num  = cards.text[:2]
                name = cards.text[3:].strip()
            
            card = Card(num, name, idDeck, board, True)

            self.setCards(card)

    # set deck on database
    def setDeck(self, idDeck, deckHref, idPlayer, isMtgDecks):
        # delete previous results before upload all deck
        self.deleteDeckCards(idDeck)
        # scrap deck
        if not isMtgDecks:
            self.getDeck(idDeck, deckHref)
            self.saveDeckCardsList()

        self.updateCardsLoaded(idDeck)
        self.updateDeckPlayer(idDeck, idPlayer)

    # save deck name
    def saveDeck(self, name):
        item     = { "name" : name }
        response = self.db.insert(deckTable, item)

        return response.data

    # save deck list on DB
    def saveDeckCardsList(self):
        for card in self.cards:
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