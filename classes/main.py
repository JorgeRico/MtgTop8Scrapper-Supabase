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

        print('\n     * Scrapping Finished !!! :D\n')

    # scrapping Tournament info and top 8 players
    def scrappingTournament(self, idTournament, name, idLeague, isMtgDecks):

        if not isMtgDecks:
            mtgTop8 = MtgTop8(idTournament)
            id      = mtgTop8.run(name, idLeague)

        print('\n     * check on: https://mtg-stats.vercel.app/tournaments/%s' %id)
            
    # update card image url
    def updateBlankImgUrls(self):
        card   = Card()
        result = card.checkCardsImgUrls()

        print('   - Updating blank imgUrls on cards table')
        for item in result:
            print('    - Cards updated: %s' %item.get('name'))
            card.updateCardData(item.get('name'))
