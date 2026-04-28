class MtgDecks:
    def __init__(self):
        self.mtgdecks = 'https://mtgdecks.net/Legacy'
 
    # card mtgdecks url
    def getScryfallUrlCardData(self, id):
        return self.mtgdecks + '/liga-de-legacy-del-valles-tournament-' + id
