from classes.league import League
from classes.tournament import Tournament
from classes.card import Card
from classes.websites.mtgTop8 import MtgTop8
 
class Main():
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def run(self):
        for item in self.tournaments:
            print('   - Scrapping : %s' %(item['name']))

            for id in item['ids']:
                print('     * Scrapping tournament id: %s' %(id))
                self.scrappingTournament(str(id), item['name'], item['league'], item['isMtgDecks'])

    # scrapping Tournament info and top 8 players
    def scrappingTournament(self, idTournament, name, idLeague, isMtgDecks):
        tournament = Tournament(idTournament, name, idLeague, True)

        if not isMtgDecks:
            mtgTop8 = MtgTop8(idTournament)
            soup = mtgTop8.getSoupData()
            # get data
            mtgTop8.getTournamentData(tournament, soup)
            # top 8 players, decks and cards
            mtgTop8.setTop8PlayersAndDecks(soup, tournament.getId())

    # update card image url
    def updateBlankImgUrls(self):
        card   = Card()
        result = card.checkCardsImgUrls()

        print('   - Updating blank imgUrls on cards table')
        for item in result:
            print('    - Cards updated: %s' %item.get('name'))
            card.updateCardData(item.get('name'))
