from classes.card import Card
from functions.db import Db
from data.tableNames import deckTable, cardsTable

class Deck:
    def __init__(self):
        self.cards = []

    def getDeckCards(self):
        return self.cards

    # scrap deck info
    def getDeck(self, idDeck, soup):
        for cards in soup.findAll('div', attrs={"class": 'deck_line hover_tr'}):
            board = cards.get('id')[:2]

            if cards.text[1] == ' ':
                num  = cards.text[0]
                name = cards.text[2:].strip()
            if cards.text[2] == ' ':
                num  = cards.text[:2]
                name = cards.text[3:].strip()
            
            card = Card(num, name, idDeck, board)
            card.setCardTypeAndImage(name)

            self.cards.append(card)

        # save entire deck
        self.saveDeckCardsList()      

    # save deck name
    def saveDeck(self, name):
        db = Db()

        item = {
            "name" : name,
        }

        response = db.insert(deckTable, item)

        return response.data

    # save deck list on DB
    def saveDeckCardsList(self):
        db = Db()

        for card in self.cards:
            item = {
                "name"     : card.getName().strip(),
                "num"      : card.getNum(),
                "idDeck"   : card.getIdDeck(),
                "board"    : card.getBoard(),
                "cardType" : card.getCardType(),
                "imgUrl"   : card.getImgUrl()
            }

            db.insert(cardsTable, item)

    # save player idDeck on DB
    def updateCardsLoaded(self, idDeck):
        db = Db()

        db.update(deckTable, {'cardsLoaded': True}, 'id', idDeck)

    # save player on DB
    def updateDeckPlayer(self, idDeck, idPlayer):
        db = Db()

        db.update(deckTable, {'idPlayer': idPlayer}, 'id', idDeck)

    # save player idDeck on DB
    def deleteDeckCards(self, idDeck):
        db = Db()

        db.delete(cardsTable, 'idDeck', idDeck)

