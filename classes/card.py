from functions.functions import Scrapping

class Card:
    def __init__(self, num, name, idDeck, board):
        self.num      = num
        self.name     = name
        self.board    = board
        self.idDeck   = idDeck
        self.cardType = None
        self.image    = None

    def getNum(self):
        return str(self.num)
    
    def getName(self):
        return str(self.name)
    
    def getBoard(self):
        return str(self.board)
    
    def getIdDeck(self):
        return self.idDeck
    
    def getCardType(self):
        return self.cardType
    
    def getImgUrl(self):
        return self.imgUrl
    
    def setCardType(self, cardType):
        self.cardType = cardType
    
    # get and set cardType and image
    def setCardTypeAndImage(self, cardName):
        soup          = Scrapping()
        cardName      = soup.convertCardName(cardName)
        soup          = soup.getJsonSoup(soup.getScryfallUrlCardData(cardName))
        self.cardType = self.getCardTypeText(soup)
        self.imgUrl   = self.setImageUrl(soup)
        
    # get cardType
    def getCardTypeText(self, soup):
        if 'planeswalker' in soup['type_line'].lower():
            return 'planeswalker'
        if 'creature' in soup['type_line'].lower():
            return 'creature'
        if 'land' in soup['type_line'].lower():
            return 'land'
        if 'artifact' in soup['type_line'].lower():
            return 'artifact'
        if 'enchantment' in soup['type_line'].lower():
            return 'enchantment'
        if 'sorcery' in soup['type_line'].lower():
            return 'sorcery'
        if 'instant' in soup['type_line'].lower():
            return 'instant'   

    # get image url
    def setImageUrl(self, soup):
        try:
            return soup['image_uris']['normal']
        except Exception:
            # double sided cards
            return soup['card_faces'][0]['image_uris']['normal']
