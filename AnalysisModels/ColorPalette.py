import colorgram

#use this, it's faster
def getColorgramPalette(baseImage):
    palette = colorgram.extract(baseImage, 5)
    hsvPalette = []
    proportions = []

    for color in palette:
        hsvPalette.append(color.hsl)
        proportions.append(color.proportion)
    
    return (hsvPalette, proportions)