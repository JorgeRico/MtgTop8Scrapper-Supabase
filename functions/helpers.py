import unidecode

class Helpers:
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
