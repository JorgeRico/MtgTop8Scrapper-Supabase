from data.tournaments import tournaments
from classes.league import League
from functions.functions import Scrapping
from classes.tournament import Tournament
from classes.top8 import Top8
from classes.card import Card

# update card image url
def updateBlankImgUrls():
    card  = Card()
    check = Scrapping()

    result = card.checkCardsImgUrls()

    print('   - Updating blank imgUrls on cards table')
    for item in result:
        print('    - Cards updated: %s' %item.get('name'))
        # bypass utf-8 error on scryfall website scrapping
        name = check.convertCardName(item.get('name'))

        url  = check.getScryfallUrlCardData(name)
        url  = check.replaceBlankSpaceUrl(url)
        soup = check.getJsonSoup(url)
        
        imgUrl = card.getImageUrl(soup)
        card.updateDeckCardsImgUrl(item.get('name'), imgUrl)


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
        idTournament = idTournament[0].get('id')
    else:
        idTournament = result[0].get('id')

    # top 8 players
    top.setTop8Players(soup, idTournament)

    # decks and cards
    top.setTop8PlayersDecks()



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

# run more than one time - supabase python has limit on select query - not group by
# updateBlankImgUrls()