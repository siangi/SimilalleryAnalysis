import csv
import sys
import os
import numpy as np
import cv2 as cv
import ImageAnalysisData
import AnalysisModels.Saliency as SaliencyModel
import AnalysisModels.HistogramOrientedGradients as HistogramModel
import AnalysisModels.ColorPalette as ColorModel

# controls the reading and writing of the csv file data
class AnalysisController:
    def __init__(self, sourceCsvPath, resultCSVPath) -> None:
        self.sourceCsvPath = sourceCsvPath
        self.resultCSVPath = resultCSVPath

    #creates reader and writer for
    def analyseImagesFromCSVFile(self):
        with open(self.sourceCsvPath, encoding="utf8") as readFile:
            reader = csv.DictReader(readFile, delimiter=";")
            with open(self.resultCSVPath, "w", encoding="utf8", newline="") as writeFile:
                writer = None
                counter = 0
                for row in reader:
                    if (writer == None):
                        headerList = row.keys()
                        headerList = self.prepareHeaderList(headerList)
                        writer = csv.DictWriter(f=writeFile, fieldnames=["Title","Year","isCentury","Artist","Category","URL","Path","saliencyCenter","saliencyRect", "angleRatios", "colorPalette", "paletteRatios"], delimiter=";")
                        writer.writeheader()

                    imgPath = self.extractPath(row)
                    if(imgPath == ""):
                        print("image skipped, does not exist. Path: " + imgPath)
                        continue
                    
                    imageData = cv.imdecode(np.fromfile(imgPath, dtype=np.uint8), cv.IMREAD_UNCHANGED)
                    # imageData = cv.pyrDown(imageData)
                    # imageData = cv.pyrDown(imageData)
                    analysisResults = self.analyseImage(imageData, imgPath)
                    writeDict = self.createResultRow(row, analysisResults)
                    writer.writerow(writeDict)
                    counter += 1
                    if counter % 10 == 0:
                        print("Images Analysed: " + str(counter))
                    


    def prepareHeaderList(self, sourceHeader):
        dummy = ImageAnalysisData.ImageAnalysisData()
        analysisHeaders = list(vars(dummy).keys())
        listHeader = list(sourceHeader)
        listHeader.extend(analysisHeaders)
        return listHeader

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

    def createResultRow(self, sourceRow, analysisResult):
        sourceRow.update(vars(analysisResult))
        return sourceRow

#D:/Studium/Bachelor/ArtVeeDataFull/artvee.csv       
#D:/Studium/Bachelor/ArtVeeDataFull/analysisResult.csv
if __name__ == "__main__":
    # if (len(sys.argv) != 3):
    #     raise Exception("script can only be called with 2 Arguments. InputCSV Path and OutputCSV Path!")
    
    # Controller = AnalysisController(sys.argv[1], sys.argv[2])
    Controller = AnalysisController("D:/Studium/Bachelor/artveeTogether.csv", "D:/Studium/Bachelor/analysisResult.csv")
    Controller.analyseImagesFromCSVFile()
    