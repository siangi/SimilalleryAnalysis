import csv
import sys
import os
import numpy as np
import cv2 as cv
import MetadataUtils
import ImageAnalysisData
import AnalysisModels.Saliency as SaliencyModel
import AnalysisModels.HistogramOrientedGradients as HistogramModel
import AnalysisModels.ColorPalette as ColorModel
from Writers.CSVWriter import CSVWriter
from Writers.DatabaseWriter import MySqlWriter

# controls the reading and writing of the csv file data
class AnalysisController:
    def __init__(self, sourceCsvPath, resultCSVPath) -> None:
        self.sourceCsvPath = sourceCsvPath
        self.resultCSVPath = resultCSVPath

    #creates reader and writer and executes them for each row in the sourceCSV
    def analyseImagesFromCSVFile(self):
        with open(self.sourceCsvPath, encoding="utf8") as readFile:
            reader = csv.DictReader(readFile, delimiter=";")
            writer = MySqlWriter()
            writer.prepare()

            counter = 0
            for row in reader:
                imgPath = self.extractPath(row)
                try:
                    if(imgPath == ""):
                        print("image skipped, does not exist. Path: " + imgPath)
                        continue
                    
                    imageData = cv.imdecode(np.fromfile(imgPath, dtype=np.uint8), cv.IMREAD_UNCHANGED)
                    analysisResults = self.analyseImage(imageData, imgPath)
                    artistBioData = MetadataUtils.splitBioString(row["Artist"])
                    row = MetadataUtils.updateYearIfNecessary(row, artistBioData)
                    writer.writeRow(row, analysisResults, artistBioData)
                except Exception as err:
                    print("error has occured" + str(err))
                
                counter += 1
                if counter % 10 == 0:
                    print("Images Analysed: " + str(counter))

            writer.cleanup()

    # check if image Path exists.    
    def extractPath(self, row):
        imgPath = row["Path"]
        if (not os.path.exists(imgPath)):
            imgPath == ""

        return imgPath

    #opensImage, controls all of the analysis, writes result into a ImageData Object
    def analyseImage(self, imgData,imgPath):
        analysisResults = ImageAnalysisData.ImageAnalysisData()

        saliencyModel = SaliencyModel.SaliencyAnalyser()
        saliencyData = saliencyModel.saliencyDataFromImage(imgData, True)
        analysisResults.setSaliencyRect(saliencyData[0])
        analysisResults.setSaliencyCenter(saliencyData[1])

        histogramModel = HistogramModel.GradientHistogramAnalyser()
        histogramRatios = histogramModel.calcHoGData(imgData)
        analysisResults.setAngleRatios(histogramRatios)

        colorPalette, colorRatios = ColorModel.getColorgramPalette(imgPath)
        analysisResults.setColorPalette(colorPalette)
        analysisResults.setPaletteRatios(colorRatios)

        return analysisResults

if __name__ == "__main__":
    # change the paths to run your own analysis
    Controller = AnalysisController("C:/Studium/BPROJ/artveeTogetherNewPath.csv", "C:/Studium/BPROJ/analysisResult.csv")
    Controller.analyseImagesFromCSVFile()
    