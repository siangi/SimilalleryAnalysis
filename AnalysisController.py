import csv
import os
import cv2 as cv
import ImageAnalysisData
import Saliency
# controls the reading and writing of the csv file data
class AnalysisController:
    def __init__(self, sourceCsvPath, resultCSVPath) -> None:
        self.sourceCsvPath = sourceCsvPath
        self.resultCSVPath = resultCSVPath

    #creates reader and writer for
    def analyseImagesFromCSVFile(self):
        with open(self.sourceCsvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                imgPath = self.extractPath(row)
                imageData = cv.imread(imgPath)
                self.analyseImage(imageData)


    def extractPath(row):
        imgPath = row["localPath"]
        if (os.path.exists(imgPath)):
            imgPath == ""

        return imgPath

    #opensImage, controls all of the analysis, writes result into a ImageData Object
    def analyseImage(self, imgData):
        analysisResults = ImageAnalysisData.ImageAnalysisData()

        saliencyMap = Saliency.spectralResidual(imgData, True)
        saliencyCoords = Saliency.calcSaliencyCoordinates(saliencyMap)
        analysisResults.setSaliencyRect(saliencyCoords[0])
        analysisResults.setSaliencyCenter(saliencyCoords[1])

        return analysisResults

    #maps the metadata from the CSV either to de ImageData Object or straight back to the ResultCSV
    def fillMetaDataFromCSV():
        pass

    def createResultHeader():
        pass

    def writeResultRow():
        pass

if __name__ == "__main__":
    Controller = AnalysisController("", "")
    imgData = cv.imread("C:\Studium\BPROJ\ArtVeeData\Zeilboten _1906_ .jpg")
    print(vars(Controller.analyseImage(imgData)))