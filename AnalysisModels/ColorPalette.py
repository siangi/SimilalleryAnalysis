import colorgram
from PIL import Image

#use this, it's faster
def getColorgramPalette(basePath):
    with Image.open(basePath) as img:
        img = img.reduce(4)
        palette = colorgram.extract(img, 5)
        hsvPalette = []
        proportions = []

        for color in palette:
            hsvPalette.append(color.hsl)
            proportions.append(color.proportion)
        
        return (hsvPalette, proportions)