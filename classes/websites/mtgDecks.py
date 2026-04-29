from classes.tournament import Tournament
from functions.scrapping import Scrapping
from classes.player import Player
from classes.top8 import Top8
from data.tournaments import lliga_valles
from classes.deck import Deck
from classes.card import Card
import sys

class MtgDecks:
    def __init__(self, idTournament):
        self.baseurl      = 'https://mtgdecks.net/Legacy'
        self.id           = None
        self.idTournament = idTournament
        self.players      = []
        self.eventUrl     = self.setEventUrl(idTournament)
 
    # event mtgdecks url
    def setEventUrl(self, id):
        return self.baseurl + '/liga-de-legacy-del-valles-tournament-' + id
    
    def getEventUrl(self):
        return self.eventUrl
    
    def setPlayers(self, player):
        self.players.append(player)
    
    # player deck url
    def getPlayerDeckUrl(self, url):
        url = url.replace('/Legacy', '')
        return self.baseurl + url

    def run(self, name, idLeague):
        soup = self.getSoupData()
        data = self.getTournamentData(soup)

        tournament = Tournament(self.idTournament, name, idLeague, True)
        self.tournamentData(tournament, data)
        print('       * Players:')
        dataPlayers = self.tournamentDataPlayers(soup, tournament)
        print('       * Decks:')
        self.tournamentDataDecks(dataPlayers)

        return tournament.getId()
    

    # get soup data from url
    def getSoupData(self):
        print('     * Url: %s' %(self.getEventUrl()))
        soup     = Scrapping()
        soupData = soup.getSoup(self.getEventUrl())
        
        return soupData
    
    # get data tournament from website - scrap mtgtop8
    def getTournamentData(self, soup):
        for tournamentSoup in soup.findAll("div", id="event"):
            num = 0
            for tournamentDivs in tournamentSoup.findAll("div", class_="row"):
                if num == 0:
                    if tournamentDivs.text is not None:
                        data = tournamentDivs.text.split('\n')
                        text = [item.strip() for item in data if item.strip()]
                    break
                num += 1
            break
        
        return text
    
    # common tournament data
    def tournamentData(self, tournament, data):
        dataDate       = self.getDateTournament(data)
        dataNumPlayers = self.getNumPlayersTournament(data)

        tournament.setDate(dataDate)
        tournament.setNumPlayers(dataNumPlayers)

        # mtgDecks vs mtgTop8 tournament id
        try:
            idx = lliga_valles.tournament_list_mtgdecks.index(int(tournament.getIdTournament()))
            tournament.setIdTournament(lliga_valles.tournament_list_mtgtop8[idx])
        except ValueError:
            print('******* tournament VS id value error *******')
            pass
        
        if not tournament.setTournamentIdFromDB():
            tournament.saveTournament()

    def getDateTournament(self, value):
        tournamentDate = value[4].split('-')

        day   = tournamentDate[2]
        month = tournamentDate[1]
        year  = tournamentDate[0][2] + tournamentDate[0][3]
        
        return day + '/' + month + '/' + year
    
    def getNumPlayersTournament(self, value):
        textSplit  = value[2].split(' ')
        numPlayers = textSplit[0]

        return numPlayers
    
    # players data + decknames
    def tournamentDataPlayers(self, soup, tournament):
        dataPlayers = self.getTop8Players(soup, tournament.getId())
        
        top8 = Top8()
        top8.savePlayers(dataPlayers)
        top8.setTop8PlayersIdDecks(dataPlayers)

        return dataPlayers

    # get players info and save on database
    def getTop8Players(self, soup, dbIdTournament):
        table = soup.find("table")
        names = self.getNames(table)
        decks = self.getDecks(table)

        all_players = self.getPlayers(decks, names)

        for index, player in enumerate(all_players, 1):
            item = Player(index, player['playerName'], player['deckHref'], dbIdTournament, player['deckName'])
            self.setPlayers(item)

        return self.players
    
    def getNames(self, table):
        names = []

        for row in table.find_all("tr"):
            cols = row.find_all("td")

            if len(cols) >= 2:
                data   = cols[1].get_text(" ", strip=True).split("$")
                values = data[0].split(' by ')
                names.append(values[1].strip().title())

        return names
    
    def getDecks(self, table):
        decks = []

        for link in table.find_all("a"):
            text = link.get_text(strip=True)
            href = link.get("href")
            item = {
                'deckHref' : self.getPlayerDeckUrl(href),
                'deckName' : text,
            }
            decks.append(item)

        return decks
    
    def getPlayers(self, decks, names):
        players = []

        for index, deck in enumerate(decks):
            item = {
                'playerName' : names[index],
                'deckHref'   : deck.get('deckHref'),
                'deckName'   : deck.get('deckName'),
            }
            players.append(item)

        return players

    # player decks
    def tournamentDataDecks(self, dataPlayers):
        pass
        for item in dataPlayers:
            deck   = Deck()
            result = deck.playerHasIdDeckOnDB(item.idPlayer)

            if not result[0].get('decks').get('cardsLoaded'):
                print('         - Deck saving on DB . . .')
                print('           --> %s | %s' %(result[0].get('decks').get('name'), result[0].get('name')))
                
                cards = self.getDeck(item.getPlayerIdDeck(), item.getDeckHref())
                deck.setDeck(item.getPlayerIdDeck(), cards, item.getIdPlayer())
                
                print('           --> Deck saved on DB: %s | %s' %(result[0].get('decks').get('name'), result[0].get('name')))
            else:
                print('         - Deck is on DB: %s | %s' %(result[0].get('decks').get('name'), result[0].get('name')))

    def getDeck(self, idDeck, deckHref):
        soup  = Scrapping()
        soup  = soup.getSoup(deckHref)
        cards = []
        
        for tournamentSoup in soup.findAll("div", class_="cards"):
            num = 0
            for tournamentCards in tournamentSoup.findAll("div", class_="col-sm-6"):
                if num == 0:
                    for tournamentTd in tournamentCards.findAll("td", class_="number"):
                        card = self.getScrappedCardData(tournamentTd, idDeck, "md")
                        cards.append(card)
                if num == 1:
                    for tournamentTd in tournamentCards.findAll("td", class_="number"):
                        card = self.getScrappedCardData(tournamentTd, idDeck, "sb")
                        cards.append(card)
                num += 1

        return cards
    
    def getScrappedCardData(self, item, idDeck, board):
        data = item.get_text(" ", strip=True)
        card = Card(self.getTotalNumCards(data), self.getNameCard(data), idDeck, board, True)

        return card

    def getTotalNumCards(self, item):
        data = item.split(' ')

        return data[0].strip()
    
    def getNameCard(self, item):
        data = item.split(' ')
        data.pop(0)
        name = ' '.join(str(val) for val in data)

        return name.strip()