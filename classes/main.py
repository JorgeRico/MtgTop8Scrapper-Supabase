from classes.card import Card
from classes.websites.mtgTop8 import MtgTop8
from classes.websites.mtgDecks import MtgDecks
from data.tableNames import tournamentTable
from classes.db import Db

class Main():
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.vercelUrl   = "https://mtg-stats.vercel.app/tournaments/"

    def run(self):
        for item in self.tournaments:
            print('   - Scrapping : %s' %(item['name']))

            for id in item['ids']:
                print('     * Scrapping tournament id: %s' %(id))
                self.scrappingTournament(str(id), item['name'], item['league'], item['isMtgDecks'])
                print('\n')

        print('     *** Scrapping Finished !!! :D ***\n')

    # scrapping Tournament info and top 8 players
    def scrappingTournament(self, idTournament, name, idLeague, isMtgDecks):
        # mtgDecks or mtgTop8 depends on tournament info
        if not isMtgDecks:
            mtgTop8 = MtgTop8(idTournament)
            id      = mtgTop8.run(name, idLeague)
        else:
            mtgDecks = MtgDecks(idTournament)
            id       = mtgDecks.run(name, idLeague)

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