
# artists name are typically like this Firstname Lastname(Nationality, YEAR BORN - YEAR DIED)
# coded partly by chatGPT, but tested by myself
def splitBioString(bioString: str):
    if(bioString.strip() == ""):
        return("Anonymous", "")
    # Split the string into components using parentheses and commas
    components = bioString.split('(')
    name = components[0].strip()
    nationality = ''

    if len(components) > 1:
        nationality = components[-1].strip(')').split(',')[0].strip()

    return (name, nationality)
