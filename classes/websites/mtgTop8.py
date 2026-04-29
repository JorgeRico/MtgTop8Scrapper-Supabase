from functions.scrapping import Scrapping
from classes.player import Player
from classes.card import Card
from classes.tournament import Tournament
from classes.deck import Deck
from classes.top8 import Top8

class MtgTop8:
    def __init__(self, idTournament):
        self.baseurl      = 'https://www.mtgtop8.com/event'
        self.id           = None
        self.idTournament = idTournament
        self.players      = []
        self.eventUrl     = self.setEventUrl(idTournament)
    
    def setPlayers(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players

    # set tournament url
    def setEventUrl(self, url):
        return self.baseurl + '?e=' + url + '&f=LE'
    
    # get tournament url
    def getEventUrl(self):
        return self.eventUrl
    
    # player deck url
    def getPlayerDeckUrl(self, url):
        return self.baseurl + url
    
    # get soup data from url
    def getSoupData(self):
        print('     * Url: %s' %(self.getEventUrl()))
        soup     = Scrapping()
        soupData = soup.getSoup(self.getEventUrl())
        
        return soupData
    
    def getDateTournament(self, value):
        textSplit      = value.split(' - ')
        tournamentDate = textSplit[1]
        
        return tournamentDate
    
    def getNumPlayersTournament(self, value):
        textSplit  = value.split(' - ')
        numPlayers = textSplit[0].replace('players', '')

        return numPlayers
    
    # get data tournament from website - scrap mtgtop8
    def getTournamentData(self, soup):
        for tournamentSoup in soup.findAll('div', attrs={"class": 'S14'}):
            num = 0
            for tournamentDivs in tournamentSoup.findAll('div'):
                if num == 1:
                    if tournamentDivs.text is not None:
                        text = tournamentDivs.text
                    break
                num += 1
            break
        
        return text

    # get players info and save on database
    def getTop8Players(self, soup, dbIdTournament):
        first_player = self.scrapTopPlayers(soup, "chosen_tr")
        all_players = self.scrapTopPlayers(soup, "hover_tr")

        all_players.insert(0, first_player[0])

        for index, player in enumerate(all_players, 1):
            item = Player(index, player['playerName'], player['deckHref'], dbIdTournament, player['deckName'])
            self.setPlayers(item)

        return self.players

    # scrap players
    def scrapTopPlayers(self, soup, className):
        players = []
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
                item = {
                    'playerName' : playerName,
                    'deckHref'   : self.getPlayerDeckUrl(deckHref),
                    'deckName'   : deckName
                }

                players.append(item)

                deckName   = ''
                playerName = ''
                deckHref   = ''
        
        return players

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

    def getDeck(self, idDeck, deckHref):
        soup  = Scrapping()
        soup  = soup.getSoup(deckHref)
        cards = []

        for cardsData in soup.findAll('div', attrs={"class": 'deck_line hover_tr'}):
            board = cardsData.get('id')[:2]

            if cardsData.text[1] == ' ':
                num  = cardsData.text[0]
                name = cardsData.text[2:].strip()
            if cardsData.text[2] == ' ':
                num  = cardsData.text[:2]
                name = cardsData.text[3:].strip()
            
            card = Card(num, name, idDeck, board, True)

            cards.append(card)

        return cards
    
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
    
    # common tournament data
    def tournamentData(self, tournament, data):
        dataDate       = self.getDateTournament(data)
        dataNumPlayers = self.getNumPlayersTournament(data)

        tournament.setDate(dataDate)
        tournament.setNumPlayers(dataNumPlayers)

        if not tournament.setTournamentIdFromDB():
            tournament.saveTournament()

    # players data + decknames
    def tournamentDataPlayers(self, soup, tournament):
        dataPlayers = self.getTop8Players(soup, tournament.getId())
        
        top8 = Top8()
        top8.savePlayers(dataPlayers)
        top8.setTop8PlayersIdDecks(dataPlayers)

        return dataPlayers
    
    # player decks
    def tournamentDataDecks(self, dataPlayers):
        for item in dataPlayers:
            deck   = Deck()
            result = deck.playerHasIdDeckOnDB(item.idPlayer)

            if not result[0].get('decks').get('cardsLoaded'):
                print('         - Deck saving on DB . . .')
                print('           --> %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
                
                cards = self.getDeck(item.getPlayerIdDeck(), item.getDeckHref())
                deck.setDeck(item.getPlayerIdDeck(), cards, item.getIdPlayer())
                
                print('           --> Deck saved on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
            else:
                print('         - Deck is on DB: %s - %s' %(result[0].get('decks').get('name'), result[0].get('name')))
