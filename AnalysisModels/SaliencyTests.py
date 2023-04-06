import unittest
import numpy.testing as nptesting
from Saliency import SaliencyAnalyser
import cv2 as cv

class TestSaliencyModel(unittest.TestCase):
    def testLargestContourArea(self):
        
        pass

    def testCalcCoordinates(self):
        pass

    def testSpectralResidual(self):
        base = cv.imread(".\\TestResources\\baseImage.jpg")
        model = SaliencyAnalyser()
        actual = model.saliencyDataFromImage(base, True)
        expected = ((54, 41, 41, 78), (74.5, 80.0))
        expectedShape = (200, 124)
        self.assertTupleEqual(actual[0], expected[0])
        self.assertTupleEqual(actual[1], expected[1])
        self.assertTupleEqual(model.getSaliencyMap().shape, expectedShape)


if __name__ == '__main__':
    unittest.main()