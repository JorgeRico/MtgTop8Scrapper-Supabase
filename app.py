from data.tournaments import lliga_catalana, lliga_minoria, lliga_valles, test_league
from classes.main import Main

if __name__ == "__main__":
    # lliga_catalana.tournament, lliga_minoria.tournament, lliga_valles.tournament
    # test_league.tournament
    tournaments = [
        lliga_catalana.tournament, lliga_minoria.tournament, lliga_valles.tournament
    ]
    main = Main(tournaments)
    main.run()

    # run more than one time - supabase python has limit on select query - not group by
    # main.updateBlankImgUrls()