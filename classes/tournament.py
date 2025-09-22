from functions.db import Db
from data.tableNames import tournamentTable

class Tournament():
    # get data tournament from website - scrap mtgtop8
    def getTournamentData(self, soup, idTournament, tournamentName, idLeague):
        for tournament in soup.findAll('div', attrs={"class": 'S14'}):
            num = 0
            for tournamentDivs in tournament.findAll('div'):
                if num == 1:
                    if tournamentDivs.text is not None:
                        text           = tournamentDivs.text
                        textSplit      = text.split(' - ')
                        tournamentDate = textSplit[1]
                        players        = textSplit[0].replace('players', '')
                    break
                num += 1
            break

        return self.saveTournament(idTournament, tournamentName, tournamentDate, idLeague, players)
    
    # save tournament on DB
    def saveTournament(self, idTournament, name, date, idLeague, players):
        db         = Db()
        item = {
            "idTournament" : idTournament,
            "name"         : name,
            "date"         : date,
            "idLeague"     : idLeague,
            "players"      : players
        }
        
        db.insert(tournamentTable, item)
    
    # check if exists tournament
    def existsTournamentOnDB(self, idTournament):
        db       = Db()
        response = db.getTableDataQueryWhere(tournamentTable, 'id', 'idTournament', idTournament)

        return response
