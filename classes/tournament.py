from classes.db import Db
from data.tableNames import tournamentTable

class Tournament():
    def __init__(self, idTournament,name, idLeague, date = "", players = []):
        # id from database
        self.id           = None
        self.name         = name
        self.date         = date
        self.idLeague     = idLeague
        self.players      = players
        # old id from access data or id from scrapping
        self.idTournament = idTournament

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id
    
    def getIdTournament(self):
        return self.idTournament
    
    def setIdTournament(self, idTournament):
        self.idTournament = idTournament
    
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
    
    def setNumPlayers(self, players):
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
    
    # save tournament on DB
    def saveTournament(self):
        db     = Db()
        result = db.insert(tournamentTable, self.getTournamentItem())
        self.setId(result.data[0].get('id'))
    
    # check if exists tournament
    def existsTournamentOnDB(self, idTournament):
        db       = Db()
        response = db.getTableDataQueryWhere(tournamentTable, 'id', 'idTournament', idTournament)

        return response
    
    # get idTournament from DB and set id if exists
    def setTournamentIdFromDB(self):
        id = self.existsTournamentOnDB(self.idTournament)

        if len(id) != 0:
            self.setId(id[0].get('id'))
            return True
        
        return False