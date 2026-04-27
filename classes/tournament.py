from classes.db import Db
from data.tableNames import tournamentTable
from functions.scrapping import Scrapping
from classes.mtgTop8 import MtgTop8

class Tournament():
    def __init__(self, id, name, idLeague, date = "", idTournament = None, players = []):
        self.id           = str(id[0] if isinstance(id, tuple) else id)
        self.name         = name
        self.date         = date
        self.idLeague     = idLeague
        self.players      = players

        self.setIdTournament(idTournament)

    def getId(self):
        return self.id
    
    def getSoupData(self):
        soup     = Scrapping()
        mtgtop8  = MtgTop8()
        soupData = soup.getSoup(mtgtop8.getEventUrl(self.id))
        
        return soupData
    
    def getIdTournament(self):
        return self.idTournament
    
    def setIdTournament(self, idTournament = None):
        if idTournament is not None: 
            self.idTournament = idTournament
        else:
            self.idTournament = str(self.id[0] if isinstance(self.id, tuple) else self.id)
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

    def getDate(self):
        return self.date
    
    def setDate(self, date):
        self.date = date
    
    def getIdLeague(self):
        return self.idLeague
    
    def setIdLeague(self, idLeague):
        self.idLeague = idLeague
    
    def getPlayers(self):
        return self.players
    
    def setPlayers(self, players):
        self.players = players

    def getTournamentItem(self):
        item = {
            "idTournament" : self.idTournament,
            "name"         : self.name,
            "date"         : self.date,
            "idLeague"     : self.idLeague,
            "players"      : self.players
        }

        return item

    # get data tournament from website - scrap mtgtop8
    def getTournamentData(self, soup):
        for tournament in soup.findAll('div', attrs={"class": 'S14'}):
            num = 0
            for tournamentDivs in tournament.findAll('div'):
                if num == 1:
                    if tournamentDivs.text is not None:
                        text        = tournamentDivs.text
                        textSplit   = text.split(' - ')
                        textDate    = textSplit[1]
                        textPlayers = textSplit[0].replace('players', '')
                    break
                num += 1
            break

        # set extra tournament data
        self.setDate(textDate)
        self.setPlayers(textPlayers)
        if not self.setTournamentIdFromDB():
            self.saveTournament()
    
    # save tournament on DB
    def saveTournament(self):
        db = Db()
        db.insert(tournamentTable, self.getTournamentItem())
    
    # check if exists tournament
    def existsTournamentOnDB(self, idTournament):
        db       = Db()
        response = db.getTableDataQueryWhere(tournamentTable, 'id', 'idTournament', idTournament)

        return response
    
    # get idTournament from DB
    def setTournamentIdFromDB(self):
        idTournament = self.existsTournamentOnDB(self.id)

        if len(idTournament) != 0:
            self.setIdTournament(idTournament[0].get('id'))
            return True
        
        return False