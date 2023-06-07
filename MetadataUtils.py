import math
import statistics
import re
# artists name are typically like this Firstname Lastname(Nationality, YEAR BORN - YEAR DIED)
# coded partly by chatGPT, but tested by myself
def splitBioString(bioString: str) -> tuple:
    if(bioString.strip() == ""):
        return("Anonymous", "", -1, -1)
    # Split the string into components using parentheses and commas
    components = bioString.split('(')
    name = components[0].strip()
    nationality = ''
    birthyear = -1
    deathyear = -1

    if len(components) > 1:
        nationality, years = components[-1].strip(')').split(',')

        yearsArr = re.split("-|–", years)
        birthyear = toIntWithDefault(yearsArr[0].strip(), -1)
        if(len(yearsArr) > 1):
            deathyear = toIntWithDefault(yearsArr[1].strip(), -1)

    return (name, nationality, birthyear, deathyear)

def toIntWithDefault(toConvert: str, default: int) -> int:
    try:
        return int(toConvert)
    except ValueError:
        return default
    

def getAverageOrPlusMinus20(firstyear: int, secondyear:int ) -> int:
    if(firstyear > 0 and secondyear > 0):
        return math.floor(statistics.mean([firstyear, secondyear]))
    elif(firstyear > 0):
        return firstyear + 20
    elif(secondyear > 0):
        return secondyear - 20
    else:
        return -1
    

def updateYearIfNecessary(baseRow: dict, artistBioData: tuple) -> dict:
    if (toIntWithDefault(baseRow["Year"], -1) <= 0):
        baseRow["Year"]  = str(getAverageOrPlusMinus20(artistBioData[2], artistBioData[3]))

    return baseRow
