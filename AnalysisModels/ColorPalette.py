import colorgram
import numpy as np
from PIL import Image

# returns top 5 colors in a tuple and how much relative space they occupy in an image as a tuple. 
def getColorgramPalette(basePath: str) -> tuple:
    # cologram works with a different image format than the other frameworks, so I need to load it again.
    with Image.open(basePath) as img:
        img = img.reduce(2)
        palette = colorgram.extract(img, 5)
        hsvPalette = []
        proportions = []

        palette.sort(key=lambda color: color.proportion, reverse=True)

        for color in palette:
            hsvPalette.append(rescaleHSLValues(color.hsl))
            proportions.append(color.proportion)
        
        return (hsvPalette, proportions)
    
# colorgram extract all values on a scale of 0,255 but the normal hsl values are within a different scale
def rescaleHSLValues(originalVals):
    return {
        "h": np.floor(np.interp(originalVals.h, [0,255], [0,360])),
        "s": np.floor(np.interp(originalVals.s, [0,255], [0,100])),
        "l": np.floor(np.interp(originalVals.l, [0,255], [0,100]))
    }

