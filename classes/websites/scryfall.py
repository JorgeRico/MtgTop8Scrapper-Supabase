class Scryfall:
    def __init__(self):
        self.scryfall = 'https://api.scryfall.com/cards'
 
    # card scryfall url
    def getScryfallUrlCardData(self, name):
        # before we use "exact", now "fuzzy"
        return self.scryfall + '/named?fuzzy=' + name
