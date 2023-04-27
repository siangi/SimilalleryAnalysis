import unittest
import MetadataUtils

class TestMetadataUtils(unittest.TestCase):
    def testSplitBioString(self):
        testCases = [
            {"input": "Francesco Lorenzi (Italian, 1723-1787)", 
             "expectedName": "Francesco Lorenzi",
             "expectedNationality": "Italian"},
            {"input": "", 
             "expectedName": "Anonymous",
             "expectedNationality": ""},
            {"input": "Ivan Pavlovich Pokhitonov (Ukrainian, 1851 - ?)", 
             "expectedName": "Ivan Pavlovich Pokhitonov",
             "expectedNationality": "Ukrainian"},
            {"input": "Carel Adolph Lion Cachet", 
             "expectedName": "Carel Adolph Lion Cachet",
             "expectedNationality": ""},            
            {"input": "Carel Adolph Lion Cachet (jun) (American, 1991-1993)", 
             "expectedName": "Carel Adolph Lion Cachet",
             "expectedNationality": "American"},                   
            {"input": "Anonymous", 
             "expectedName": "Anonymous",
             "expectedNationality": ""},                   
        ]
        for test in testCases:
            actualOutput = MetadataUtils.splitBioString(test["input"])
            self.assertEqual(test["expectedName"], actualOutput[0])
            self.assertEqual(test["expectedNationality"], actualOutput[1])
