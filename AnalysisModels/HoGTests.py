import unittest
import numpy.testing as nptesting
from HistogramOrientedGradients import GradientHistogramAnalyser
import skimage.io


class TestHOG(unittest.TestCase):
    def testFullService(self):
        base = skimage.io.imread(".\\TestResources\\HogTest.png")
        EXPECTED = [0.0, 0.0, 0.0, 0.0, 0.007, 0.0, 0.993, 0.0]
        model = GradientHistogramAnalyser()
        nptesting.assert_array_equal(model.calcHoGData(base), EXPECTED)

    def testLargestInEachCell(self):
        testCases = (
            ([[[[[0, 1, 0, 0, 0, 0, 0, 0]]], [[[0, 1, 0, 0, 0, 0, 0, 0]]], [[[0, 1, 0, 0, 0, 0, 0, 0]]]]], 
                [0, 3, 0, 0, 0, 0, 0, 0]),
            ([[[[[1, 1, 1, 1, 1, 1, 1, 1]]], [[[0, 1, 0, 0, 0, 0, 0, 0]]], [[[0, 1, 0, 0, 0, 0, 0, 0]]]]], 
                [1, 3, 1, 1, 1, 1, 1, 1]),
            ([[[[[1, 5, 1, 6, 1, 1, 1, 1]]], [[[0, 1, 0, 0, 0, 0, 0, 0]]], [[[0, 0, 0, 0, 0, 0, 8, 0]]]]], 
                [0, 1, 0, 1, 0, 0, 1, 0]),
            ([[[[[5, 5, 5, 6, 1, 1, 1, 1]]], [[[5, 5, 5, 5, 5, 0, 0, 0]]], [[[0, 0, 0, 0, 0, 0, 3, 0]]]]], 
                [1, 1, 1, 2, 1  , 0, 1, 0])
        )
        model = GradientHistogramAnalyser()
        for test in testCases:
            nptesting.assert_array_equal(model._largestInEachCell(test[0]), test[1])


    def testNormaliseArrayValues(self):
        testCases = (
            ([100, 110, 133, 124], [0, 10, 33, 24]),
            ([0, 120, 130, 140], [0, 120, 130, 140]),
            ([200, 200, 330, 300], [0,0, 130, 100])
        )
        model = GradientHistogramAnalyser()
        for test in testCases:
            self.assertEqual(model._normaliseArrayValues(test[0]), test[1])

    def testRelativeToSum(self):
        testCases = (
            ([20, 20, 20, 20, 20], [0.20, 0.20, 0.20, 0.20, 0.20]),
            ([100, 0, 50], [0.667, 0, 0.333]),
            ([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4]),
        )
        model = GradientHistogramAnalyser()
        for test in testCases:
            self.assertEqual(model.relativeToSum(test[0]), test[1])

if __name__ == '__main__':
    unittest.main()