import numpy as np
import math
import cv2 as cv
import os

# Model for image Saliency Analysis 
class SaliencyAnalyser:

    def __init__(self, saliencyMap=None) -> None:
        self.saliencyMap = saliencyMap

    def setSaliencyMap(self, map):
        self.saliencyMap = map

    def getSaliencyMap(self):
        if not np.any(self.saliencyMap):
            raise AttributeError("SaliencyMap doesn't exist, please calculate it with one of the functions first")
    
        return self.saliencyMap

    # uses the spectralResidual Algorithm for Saliency detection
    # returns coordinates and bounding of largest salient region
    # and saves the saliency map to a member variable
    def saliencyDataFromImage(self, baseImage, downscale):
        self.spectralResidual(baseImage, downscale)
        return self.calcSaliencyCoordinates(self.getLargestContourArea(self.saliencyMap), self.saliencyMap.shape)

    #grabCut Slaiency Method returns foreground with all pxiels visible
    def grabCut(self, img, downscale):

        #reduce the resolution for faster runtime
        if(downscale):
            img = cv.pyrDown(img, img, (0,0), cv.BORDER_DEFAULT)
            img = cv.pyrDown(img, img, (0,0), cv.BORDER_DEFAULT)


        #empty parameters for grabcut
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64) 

        #only stuff inside this frame can be foreground
        searchRect = (10,10,img.shape[1] - 10,img.shape[0] - 10)

        # calc GrabCut
        cv.grabCut(img,mask,searchRect,bgdModel,fgdModel,3, cv.GC_INIT_WITH_RECT)   
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        self.saliencyMap = img
        return img

    #spectralResiudal Saliency Method, returns binary Saliency Map
    #is default Saliency Method because it produces the best results
    def spectralResidual(self, img, downscale):
        #for better performance
        if(downscale):
            img = cv.pyrDown(img, (0,0))
            img = cv.pyrDown(img, (0,0))

        detector = cv.saliency.StaticSaliencySpectralResidual_create()
        (success, map) = detector.computeSaliency(img)
        map = (map * 255).astype("uint8")
        threshMap = cv.threshold(map.astype("uint8"), 0, 255,
        cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        self.saliencyMap = threshMap
        return threshMap

    #finegrained Saliency Method, returns binary Saliency Map
    def fineGrained(self, img, downscale):
        if(downscale):
            img = cv.pyrDown(img, (0,0))
            img = cv.pyrDown(img, (0,0))

        detector = cv.saliency.StaticSaliencyFineGrained_create()
        (success, map) = detector.computeSaliency(img)
        map = (map * 255).astype("uint8")
        threshMap = cv.threshold(map.astype("uint8"), 0, 255,
        cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

        self.saliencyMap = threshMap
        return threshMap

    #requires a binary image, returns a polygon which represents largest white area in picture
    def getLargestContourArea(self, img):
        largestContour = None
        largestArea = -1.1
        
        contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            currentArea = cv.contourArea(contour)
            if (currentArea > largestArea):
                largestArea = currentArea
                largestContour = contour

        return largestContour

    #returns bounding rectangle (x,y, width, height)[0] and its centerpoint[1] from a binary saliency Map
    def calcSaliencyCoordinates(self, contour, imageDimensions):
        bounds = cv.boundingRect(contour)
        #rescale values to be a percentage. For comparison across different image formats
        scaledBounds = (
            int(np.floor(np.interp(bounds[0], [0,imageDimensions[0]], [0,100]))),
            int(np.floor(np.interp(bounds[1], [0, imageDimensions[1]], [0, 100]))),
            int(np.floor(np.interp(bounds[2], [0,imageDimensions[0]], [0,100]))),
            int(np.floor(np.interp(bounds[3], [0, imageDimensions[1]], [0, 100])))
        )
        centerX = scaledBounds[0] + math.floor(scaledBounds[2] / 2)
        centerY = scaledBounds[1] + math.floor(scaledBounds[3] / 2)

        return (scaledBounds, (centerX, centerY))
    
