import unittest
import numpy as np
import numpy.testing as nptesting
from AnalysisModels.Saliency import SaliencyAnalyser
import cv2 as cv

class TestSaliencyModel(unittest.TestCase):
    def testLargestContourArea(self):
        EXPECTED_CONTOURS = [[[391, 419]], [[391, 799]], [[799, 799]], [[799, 419]]]
        model = SaliencyAnalyser()
        base = cv.imread(".\\Tests\\TestResources\\ContourArea.png", cv.IMREAD_GRAYSCALE)
        actualContours = model.getLargestContourArea(base)
        self.assertEqual(len(actualContours), len(EXPECTED_CONTOURS))

        for boxedIdx in range(len(EXPECTED_CONTOURS)):
            nptesting.assert_array_equal(actualContours[boxedIdx][0], EXPECTED_CONTOURS[boxedIdx][0])
        

    def testCalcCoordinates(self):
        CONTOURS = np.array([[[0, 0]], [[0, 100]], [[100, 100]], [[100, 0]]])
        imgDimensions = (200, 200)
        expectedRect = (0, 0, 50, 50)
        expectedCenter = (25, 25)
        model = SaliencyAnalyser()
        actualCoordinates = model.calcSaliencyCoordinates(CONTOURS, imgDimensions)
        self.assertTupleEqual(actualCoordinates[0], expectedRect)
        self.assertTupleEqual(actualCoordinates[1], expectedCenter)

    def testSpectralResidual(self):
        base = cv.imread(".\\Tests\\TestResources\\baseImage.jpg")
        model = SaliencyAnalyser()
        actual = model.saliencyDataFromImage(base, True)
        expected = ((27, 33, 20, 62), (37, 64))
        expectedShape = (200, 124)
        self.assertTupleEqual(actual[0], expected[0])
        self.assertTupleEqual(actual[1], expected[1])
        self.assertTupleEqual(model.getSaliencyMap().shape, expectedShape)

if __name__ == '__main__':
    unittest.main()
