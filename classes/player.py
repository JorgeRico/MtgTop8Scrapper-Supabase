from functions.db import Db
from data.tableNames import playerTable

class Player:
    def __init__(self, num, playerName, deckHref, idTournament, deckName, idPlayer = None):
        self.num          = num
        self.playerName   = playerName
        self.deckName     = deckName
        self.deckHref     = deckHref
        self.cards        = None
        self.idPlayer     = idPlayer
        self.idTournament = idTournament
    
    def getPlayerNum(self):
        return str(self.num)
    
    def getPlayerName(self):
        return str(self.playerName)
    
    def getPlayerDeckName(self):
        return str(self.deckName)
    
    def getPlayerDeckHref(self):
        return str(self.deckHref)
    
    def getPlayerDeck(self):
        return self.cards
    
    def getPlayerTournament(self):
        return self.idTournament
    
    def getDeckHref(self):
        return self.deckHref
    
    def getIdPlayer(self):
        return self.idPlayer

    def getIdPlayer(self):
        return self.idPlayer

    def setIdPlayer(self, idPlayer):
        self.idPlayer = idPlayer

    # save player on DB
    def savePlayer(self):
        db   = Db()

        item = {
            "name"         : self.getPlayerName(),
            "position"     : self.getPlayerNum(),
            "idTournament" : self.getPlayerTournament(),
            "deckHref"     : self.getDeckHref()
        }

        try:
            response = db.insert(playerTable, item)

            return response.data
        except Exception:
            return None
    
    # save player idDeck on DB
    def savePlayerIdDeck(self, idDeck, idPlayer):
        db   = Db()
        item = {'idDeck': idDeck}

        try:
            db.update(playerTable, item, 'id', idPlayer)
        except Exception:
            return None

    # check if player exists on db
    def existsPlayerOnDB(self):
        db       = Db()
        supabase = db.getSupabase()

        try:
            response = supabase.table(playerTable).select('id').eq('name', self.getPlayerName()).eq('position', self.getPlayerNum()).eq('idTournament', self.getPlayerTournament()).execute()

            return response.data
        except Exception:
            return None
        
    # check if player has deck saved
    def existPlayerDeckOnDb(self, idPlayer):
        db = Db()

        try:
            response = db.getTableDataQueryWhere(playerTable, 'idDeck', 'id', idPlayer)

            return response.data
        except Exception:
            return None
    
    
