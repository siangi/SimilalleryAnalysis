import colorgram
import numpy as np
from PIL import Image

#use this, it's faster
def getColorgramPalette(basePath):
    with Image.open(basePath) as img:
        img = img.reduce(4)
        palette = colorgram.extract(img, 5)
        hsvPalette = []
        proportions = []

        for color in palette:
            hsvPalette.append(rescaleHSLValues(color.hsl))
            proportions.append(color.proportion)
        
        return (hsvPalette, proportions)
    

def rescaleHSLValues(originalVals):
    return {
        "h": np.floor(np.interp(originalVals.h, [0,255], [0,360])),
        "s": np.floor(np.interp(originalVals.s, [0,255], [0,100])),
        "l": np.floor(np.interp(originalVals.l, [0,255], [0,100]))
    }