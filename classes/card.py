from functions.scrapping import Scrapping
from functions.helpers import Helpers
from classes.db import Db
from data.tableNames import cardsTable
from classes.scryfall import Scryfall

class Card:
    def __init__(self, num = None, name = None, idDeck = None, board = None, setImageAndCardType = False):
        self.num      = num
        self.name     = name
        self.idDeck   = idDeck
        self.board    = board

        if setImageAndCardType:
            self.setCardTypeAndImage(name)
        else:
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
        helpers       = Helpers()
        scryfall      = Scryfall()

        cardName      = helpers.convertCardName(cardName)
        soup          = soup.getJsonSoup(scryfall.getScryfallUrlCardData(cardName))
        self.cardType = self.getCardTypeText(soup)
        self.imgUrl   = self.getImageUrl(soup)
        
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
    def getImageUrl(self, soup):
        try:
            return soup['image_uris']['normal']
        except Exception:
            # double sided cards
            return soup['card_faces'][0]['image_uris']['normal']
        
    # Get empty imgUrl rows - supabase python has limit on select query - not group by
    def checkCardsImgUrls(self):
        db       = Db()
        supabase = db.getSupabase()
        response = supabase.table(cardsTable).select("name").filter('imgUrl','is', 'null').execute()

        return response.data
    
    # update cards img url
    def updateDeckCardsImgUrl(self, name, url):
        db = Db()
        db.update(cardsTable, {'imgUrl': url}, 'name', name)

    def getCardItem(self):
        item = {
            "name"     : self.getName().strip(),
            "num"      : self.getNum(),
            "idDeck"   : self.getIdDeck(),
            "board"    : self.getBoard(),
            "cardType" : self.getCardType(),
            "imgUrl"   : self.getImgUrl()
        }
        
        return item
    
    def updateCardData(self, itemName):
        scrapping = Scrapping()
        helpers   = Helpers()
        scryfall  = Scryfall()

        # bypass utf-8 error on scryfall website scrapping
        name = helpers.convertCardName(itemName)

        url  = scryfall.getScryfallUrlCardData(name)
        url  = helpers.replaceBlankSpaceUrl(url)
        soup = scrapping.getJsonSoup(url)
        
        imgUrl = self.getImageUrl(soup)
        self.updateDeckCardsImgUrl(itemName, imgUrl)