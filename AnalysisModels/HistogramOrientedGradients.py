from skimage.transform import resize
import skimage.feature
from skimage.color import rgb2gray 
import numpy

class GradientHistogramAnalyser:
    def __init__(self) -> None:
        # no magic numbers
        self.ORIENTATIONS = 8
        self.PIXELS_PER_CELL = (16, 16)
        self.CELLS_PER_BLOCK = (1, 1)

    # analyses image gradients and returns the amount of times each 
    # angle of gradient is the most prominent one in a cell
    def calcHoGData(self, image):
        gray = rgb2gray(image)
        histogram = self.createGradientHistogram(gray)
        countedOrientations = self._largestInEachCell(histogram)
        return self.relativeToSum(self._normaliseArrayValues(countedOrientations))

    # analyses image gradients in cells and returns their probable orientations
    def createGradientHistogram(self, image):
        # image = resize(image, (len(image)/4, math.floor(len(image[0])/4)))
        data = skimage.feature.hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1,1), visualize=False, feature_vector=False)
        return data
    
    #creates an array which counts how many times each angle is the most prominent
    #angle in a cell. 
    def _largestInEachCell(self, fullData):        
        magnitudeIsMax = numpy.zeros((self.ORIENTATIONS))

        for row in fullData:
            for cell in row:
                #the actual cell data is nested two times
                magnitudes = cell[0][0]
                cellMaximum = max(magnitudes)
                for magnitudeIdx in range(len(magnitudes)):
                    if magnitudes[magnitudeIdx] == cellMaximum:
                        magnitudeIsMax[magnitudeIdx] += 1
        
        return magnitudeIsMax

    # in cell without a gradient, every angle is the maximum angle, so we
    # substract the minimum from all of them to ged rid of that.
    def _normaliseArrayValues(self, data):
        minimum = min(data)

        return [val - minimum for val in data]
    
    # use relative values, for easier comparison
    def relativeToSum(self,data):
        arraySum = sum(data)

        return [round(val / arraySum, 3) for val in data]