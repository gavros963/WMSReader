from wondermail.sky_dungeon import WMSkyDungeon
from wondermail.sky_item import WMSkyItem
from wondermail.sky_poke import WMSkyPoke
from wondermail.wonderMail import WMSParser

def getItemName(itemID):
    """
    Returns the name of the item given its ID.
    """
    if itemID in WMSkyItem:
        return WMSkyItem[itemID]
    else:
        return "Unknown Item"

def getDungeonName(dungeonID):
    """
    Returns the name of the dungeon given its ID.
    """
    if dungeonID in WMSkyDungeon:
        return WMSkyDungeon[dungeonID]
    else:
        return "Unknown Dungeon"

def getPokeName(pokeID):
    """
    Returns the name of the Pokémon given its ID.
    """
    female = (pokeID > 600)
    if female:
        pokeID -= 600
    if pokeID in WMSkyPoke:
        return WMSkyPoke[pokeID]
    else:
        return "Unknown Pokémon"

def prettyMailString(mailString, rows, middleColumnSize):
    mailString = WMSParser.sanitize(mailString)

    outerColumnSize = int((len(mailString) - (rows * middleColumnSize)) // (rows * 2))

    prettyString = ''
    stringPtr = 0
    for _ in range(rows):
        if prettyString != '':
            prettyString += '\n'
        prettyString += mailString[stringPtr:stringPtr + outerColumnSize] + " "
        stringPtr += outerColumnSize
        prettyString += mailString[stringPtr:stringPtr + middleColumnSize] + " "
        stringPtr += middleColumnSize
        prettyString += mailString[stringPtr:stringPtr + outerColumnSize]
        stringPtr += outerColumnSize
    return prettyString