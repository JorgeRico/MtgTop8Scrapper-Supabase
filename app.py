from data.tournaments import tournaments
from data.tableNames import tournamentTable
from classes.league import League
from functions.functions import Scrapping
from classes.tournament import Tournament
from classes.top8 import Top8

# scrapping data
def scrapping(id, name, idLeague):
    soup = Scrapping()
    top  = Top8()

    # scrapping
    soup = soup.getSoup(soup.getEventUrl(id))
    # Tournament info
    tournament = Tournament()

    # Check if tournament exists on DB
    result = tournament.existsTournamentOnDB(id)
    
    if (len(result) == 0):
        idTournament = tournament.getTournamentData(soup, id, name, idLeague)
    else:
        idTournament = result[0].get('id')

    # top 8 players
    top.setTop8Players(soup, idTournament)

    # decks and cards
    top.setTop8PlayersDecks(idTournament)



# main function
def main(tournaments):
    for item in tournaments:
        print('   - Scrapping : %s' %(item['name']))

        league = League(item['league'], item['name'], item['year'], item['isLegacy'])
        league.saveLeague()
        
        for id in item['ids']:
            print('     * Scrapping tournament id: %s' %(id))
            scrapping(str(id), item['name'], item['league'])

main(tournaments)