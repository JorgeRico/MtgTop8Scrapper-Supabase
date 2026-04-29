# tournaments
# league and name hardcoded
# ids from www.mtgtop8.com or mtgdecks.net
# ########################################################################
# IMPORTANT :
# current league needs to be changed manually on DB when new season starts
# ########################################################################
# mantain array order relation
tournament_list_mtgtop8  = [ 83134  , 81664 ]
tournament_list_mtgdecks = [ 241991 , 237093 ]

# this league sometimes has more players loaded on mtgdecks website
isMtgDecks = False

tournament = {
    'league'     : 26,
    'name'       : 'Lliga del Valles',
    'ids'        : tournament_list_mtgdecks if isMtgDecks else tournament_list_mtgtop8,
    'year'       : 2026,
    'isLegacy'   : 1,
    'isMtgDecks' : isMtgDecks
}