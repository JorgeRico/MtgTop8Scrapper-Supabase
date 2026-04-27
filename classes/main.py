from classes.league import League
from classes.tournament import Tournament
from classes.top8 import Top8
from classes.card import Card
 
class Main():
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def run(self):
        for item in self.tournaments:
            print('   - Scrapping : %s' %(item['name']))

            league = League(item['league'], item['name'], item['year'], item['isLegacy'])
            league.saveLeague()
            
            for id in item['ids']:
                print('     * Scrapping tournament id: %s' %(id))
                self.scrappingTournament(str(id), item['name'], item['league'])

    # scrapping Tournament info and top 8 players
    def scrappingTournament(self, id, name, idLeague):
        tournament = Tournament(id, name, idLeague, True)
        soup       = tournament.getSoupData()
        tournament.getTournamentData(soup)

        # top 8 players, decks and cards
        top = Top8(tournament.getIdTournament())
        top.setTop8PlayersAndDecks(soup)

    # update card image url
    def updateBlankImgUrls(self):
        card   = Card()
        result = card.checkCardsImgUrls()

        print('   - Updating blank imgUrls on cards table')
        for item in result:
            print('    - Cards updated: %s' %item.get('name'))
            card.updateCardData(item.get('name'))
