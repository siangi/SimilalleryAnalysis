import unittest
import AnalysisModels.ColorPalette as ColorPalette
import os

class TestColorPalette(unittest.TestCase):
    def testFullService(self):
        testCases = [{
                "imgName": "PaletteTestSwatch.png",        
                "expectedPalette": [{'h': 357.0, 's': 84.0, 'l': 51.0}, 
                                    {'h': 73.0, 's': 80.0, 'l': 50.0}, 
                                    {'h': 338.0, 's': 100.0, 'l': 83.0}, 
                                    {'h': 0.0, 's': 0.0, 'l': 49.0}, 
                                    {'h': 351.0, 's': 88.0, 'l': 67.0}]
            }
        ]

        for case in testCases:                        
            actualPalette = ColorPalette.getColorgramPalette(".\\Tests\\TestResources\\" + case["imgName"])
            self.assertCountEqual(actualPalette[0], case["expectedPalette"])
            for index in range(len(case["expectedPalette"])):
                self.assertDictEqual(case["expectedPalette"][index], actualPalette[0][index])



if __name__ == '__main__':
    unittest.main()        

