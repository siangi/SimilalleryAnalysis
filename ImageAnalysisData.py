class ImageAnalysisData:
    def __init__(self) -> None:
        self.saliencyCenter = (-1,-1)
        self.saliencyRect = (-1, -1, -1, -1)
        self.AngleRatios = []

    def setSaliencyCenter(self, center):
        self.saliencyCenter = center

    def setSaliencyRect(self, rect):
        self.saliencyRect = rect