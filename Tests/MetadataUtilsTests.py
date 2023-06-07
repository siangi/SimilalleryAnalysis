import unittest
import MetadataUtils

class TestMetadataUtils(unittest.TestCase):
    def testSplitBioString(self):
        testCases = [
            {"input": "Francesco Lorenzi (Italian, 1723-1787)", 
             "expectedName": "Francesco Lorenzi",
             "expectedNationality": "Italian",
             "expectedBirthyear": 1723,
             "expectedDeathyear": 1787},
            {"input": "", 
             "expectedName": "Anonymous",
             "expectedNationality": "",
             "expectedBirthyear": -1,
             "expectedDeathyear": -1},
            {"input": "Ivan Pavlovich Pokhitonov (Ukrainian, 1851 - ?)", 
             "expectedName": "Ivan Pavlovich Pokhitonov",
             "expectedNationality": "Ukrainian",
             "expectedBirthyear": 1851,
             "expectedDeathyear": -1},
            {"input": "Carel Adolph Lion Cachet", 
             "expectedName": "Carel Adolph Lion Cachet",
             "expectedNationality": "",
             "expectedBirthyear": -1,
             "expectedDeathyear": -1},            
            {"input": "Carel Adolph Lion Cachet (jun) (American, 1991–1993)", 
             "expectedName": "Carel Adolph Lion Cachet",
             "expectedNationality": "American",
             "expectedBirthyear": 1991,
             "expectedDeathyear": 1993},                               
        ]
        for test in testCases:
            actualOutput = MetadataUtils.splitBioString(test["input"])
            self.assertEqual(test["expectedName"], actualOutput[0])
            self.assertEqual(test["expectedNationality"], actualOutput[1])
            self.assertEqual(test["expectedBirthyear"], actualOutput[2])
            self.assertEqual(test["expectedDeathyear"], actualOutput[3])

    def testGetAverage(self):
        testCases = [
            { "input": (-1, -1), "expected": -1},
            { "input": (10, 20), "expected": 15},
            { "input": (10, 16), "expected": 13},
            { "input": (10, 15), "expected": 12},
            { "input": (1, -1), "expected": 21},
            { "input": (-1, 21), "expected": 1}
        ]

        for test in testCases:
            actual = MetadataUtils.getAverageOrPlusMinus20(test["input"][0], test["input"][1])
            self.assertEqual(actual, test["expected"])

    def testUpdateYearIfNecessary(self):
        testCases = [
            { "row": {"Year": "-1"}, 
             "bioData": ("name", "nation", 1720, 1740), 
             "expected": {"Year": "1730"}},
            { "row": {"Year": "1755"}, 
             "bioData": ("name", "nation", 1720, 1740), 
             "expected": {"Year": "1755"}},
            { "row": {"Year": "1999"}, 
             "bioData": ("name", "nation", 1720, 1740), 
             "expected": {"Year": "1999"}},
            { "row": {"Year": "-1"}, 
             "bioData": ("name", "nation", 0, 1740), 
             "expected": {"Year": "1720"}},
            { "row": {"Year": "0"}, 
             "bioData": ("name", "nation", 1730, 0), 
             "expected": {"Year": "1750"}},
        ]

        for test in testCases:
            actual = MetadataUtils.updateYearIfNecessary(test["row"], test["bioData"])
            self.assertDictEqual(actual, test["expected"])