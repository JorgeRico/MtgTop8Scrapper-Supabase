from classes.card import Card
from classes.websites.mtgTop8 import MtgTop8
from classes.websites.mtgDecks import MtgDecks
from data.tableNames import tournamentTable
from classes.db import Db
from functions.helpers import Helpers
import sys
class Main():
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.vercelUrl   = "https://mtg-stats.vercel.app/tournaments/"

    def run(self):
        item = self.tournaments[0]
        print('   - Scrapping : %s' %(item['name']))

        for id in self.tournaments[0]['ids']:
            if id is not None:
                print(Helpers.YELLOW + '     * Scrapping tournament id: %s' %(id) + Helpers.RESET)
                self.scrappingTournament(str(id), item)

                # exception only for lliga del valles - only if arrays have different lengths
                if item['isMtgDecks'] is True and item['isArrayLenEqual'] is False:
                    print(Helpers.RED + '\n     *** LLV exception - Tournament Array items with different lengths !!!' + Helpers.RESET)
                    print(Helpers.RED + '     *** ONLY the first mtgdecks tournament is checked !!! \n' + Helpers.RESET)
                    break
                print('\n')

        print(Helpers.GREEN + '     *** Scrapping Finished !!! :D ***\n' + Helpers.RESET)

    # scrapping Tournament info and top 8 players
    def scrappingTournament(self, idTournament, item):
        # mtgDecks or mtgTop8 depends on tournament info
        if not item['isMtgDecks']:
            mtgTop8 = MtgTop8(idTournament)
            id      = mtgTop8.run(item['name'], item['league'])
        else:
            mtgDecks = MtgDecks(idTournament, item['isArrayLenEqual'])
            id       = mtgDecks.run(item['name'], item['league'])

        print('\n     * check on: %s%s' %(self.vercelUrl ,id))
            
    # update card image url
    def updateBlankImgUrls(self):
        card   = Card()
        result = card.checkCardsImgUrls()

        print('   - Updating blank imgUrls on cards table')
        for item in result:
            print('    - Cards updated: %s' %item.get('name'))
            card.updateCardData(item.get('name'))

    # update idTournament
    # main scrapper = mtgTop8, but sometimes data is on mtgDecks before
    # update idTournaments to mantain consistency
    def updateZeroIdTournamentCreatedFromMtgDecks(self, idTournament):
        db   = Db()
        item = { 'idTournament': idTournament }

        try:
            db.update(tournamentTable, item, 'idTournament', 0)
        except Exception:
            return None