import unittest
import ColorPalette
import os


# 75, 87, 90 / 358, 88, 93 / 340, 32, 100 / 0, 0, 50


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
            actualPalette = ColorPalette.getColorgramPalette(os.getcwd() + "/TestResources/" + case["imgName"])
            self.assertCountEqual(actualPalette[0], case["expectedPalette"])
            for index in range(len(case["expectedPalette"])):
                self.assertDictEqual(case["expectedPalette"][index], actualPalette[0][index])



if __name__ == '__main__':
    unittest.main()        

