import unidecode

class Helpers:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    RESET  = '\033[0m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'

    # extrange names
    def convertCardName(self, cardName):
        cardName = unidecode.unidecode(cardName)
        cardName = cardName.replace('L 3/4rien', 'Lorien')
        cardName = cardName.replace('Lurien', 'Lorien')
        cardName = cardName.replace('LUrien', 'Lorien')
        cardName = cardName.replace('dZm', 'dum')
        cardName = cardName.replace(' ', '%20')
        cardName = cardName.replace(',', '')
        cardName = cardName.replace('&', '')

        return cardName

    def replaceBlankSpaceUrl(self, url):
        return url.replace(' ', '%20')
