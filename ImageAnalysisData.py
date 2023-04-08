class ImageAnalysisData:
    def __init__(self) -> None:
        self.saliencyCenter = (-1,-1)
        self.saliencyRect = (-1, -1, -1, -1)
        self.angleRatios = []
        self.colorPalette = []
        self.paletteRatios = []

    def setSaliencyCenter(self, center):
        self.saliencyCenter = center

    def setSaliencyRect(self, rect):
        self.saliencyRect = rect

    def setAngleRatios(self, ratios):
        self.angleRatios = ratios

    def setColorPalette(self, palette):
        self.colorPalette = palette

    def setPaletteRatios(self, ratios):
        self.paletteRatios = ratios