from classes.db import Db
from data.tableNames import leagueTable

class League:
    def __init__(self, id, name, year, isLegacy):
        self.id        = id
        self.name      = name
        self.year      = year,
        self.isLegacy  = isLegacy

    def getLeagueId(self):
        return self.id
    
    def getLeagueName(self):
        return self.name
    
    def getLeagueYear(self):
        return self.year
    
    def getLeagueITem(self):
        item = {
            "id"       : self.id,
            "name"     : self.name,
            "year"     : ' '.join(str(val) for val in self.year),
            "isLegacy" : self.isLegacy
        }

        return item

    # save league on DB
    def saveLeague(self):
        db = Db()
        db.insert(leagueTable, self.getLeagueITem())
