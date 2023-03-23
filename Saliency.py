import numpy as np
import cv2 as cv
import os
import Saliency

def grabCut(img, downscale):
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

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

    return img

def spectralResidual(img, downscale):
    if(downscale):
        img = cv.pyrDown(img, (0,0))
        img = cv.pyrDown(img, (0,0))

    detector = cv.saliency.StaticSaliencySpectralResidual_create()
    (success, map) = detector.computeSaliency(img)
    map = (map * 255).astype("uint8")
    threshMap = cv.threshold(map.astype("uint8"), 0, 255,
	cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    return threshMap

def fineGrained(img, downscale):
    if(downscale):
        img = cv.pyrDown(img, (0,0))
        img = cv.pyrDown(img, (0,0))

    detector = cv.saliency.StaticSaliencyFineGrained_create()
    (success, map) = detector.computeSaliency(img)
    map = (map * 255).astype("uint8")
    threshMap = cv.threshold(map.astype("uint8"), 0, 255,
	cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

    return threshMap

#requires a binary image
def getLargestContourArea(img):
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
def calcSaliencyCoordinates(saliencyMap):
    largestContour = getLargestContourArea(saliencyMap)
    bounds = cv.boundingRect(largestContour)
    centerX = bounds[0] + (bounds[2] / 2)
    centerY = bounds[1] + (bounds[3] / 2)
    return (bounds, (centerX, centerY))

#tries all three saliency algorithms
def testSaliencyAlgorithms(path):
    try:
        img = cv.imread(path)
        img = cv.pyrDown(img, (0,0))
        img = cv.pyrDown(img, (0,0))
    except:
        return
    

    grabCutMap = grabCut(img, False)
    grabCutBounds = cv.boundingRect(grabCutMap)

    spectralMap = spectralResidual(img, False)    
    spectralLargest = getLargestContourArea(spectralMap)
    spectralBounds = cv.boundingRect(spectralLargest)
    

    fineGrainedMap = fineGrained(img, False)
    fineLargest = getLargestContourArea(fineGrainedMap)
    fineBounds = cv.boundingRect(fineLargest)

    # show SalientMaps too
    fineGrainedMap = cv.cvtColor(fineGrainedMap, cv.COLOR_GRAY2BGR)
    cv.rectangle(fineGrainedMap, fineBounds[:2], (fineBounds[0]+fineBounds[2], fineBounds[1] + fineBounds[3]), (255, 0, 0))
    cv.drawContours(fineGrainedMap, [fineLargest], 0, (255,0,0))
    spectralMap = cv.cvtColor(spectralMap, cv.COLOR_GRAY2BGR)
    cv.drawContours(spectralMap, [spectralLargest], 0, (0,0, 255), 2)
    cv.rectangle(spectralMap, spectralBounds[:2], (spectralBounds[0]+spectralBounds[2], spectralBounds[1] + spectralBounds[3]), (0, 0, 255))
    cv.imshow("GrabCut", grabCutMap)
    cv.imshow("Spectral", spectralMap)
    cv.imshow("fineGrained", fineGrainedMap)

    #red = grabCut, green = finegrained, blue = spectral
    cv.rectangle(img, fineBounds[:2], (grabCutBounds[0] + grabCutBounds[2], grabCutBounds[1] + grabCutBounds[3]), (0, 0, 255))
    cv.rectangle(img, fineBounds[:2], (fineBounds[0] + fineBounds[2], fineBounds[1] + fineBounds[3]), (0, 255, 0))
    cv.rectangle(img, spectralBounds[:2], (spectralBounds[0]+spectralBounds[2], spectralBounds[1] + spectralBounds[3]), (255, 0, 0))

    # cv.imwrite("D:\\Studium\\Bachelor\\ArtVeeSaliencyTests\\" + os.path.basename(path), img)
    cv.imshow("original", img)
    
    cv.waitKey(0)


def testAllImagesInDirectory():
    directory = "D:\\Studium\\Bachelor\\ArtVeeData\\"

    for file in os.listdir(directory):
        filename = os.fsencode(file)
        testSaliencyAlgorithms(directory + file)



# testSaliencyAlgorithms("C:\\Studium\\BPROJ\\ArtVeeData\\1918 Opfertag (1918) .jpg")
# testSaliencyAlgorithms("C:\\Studium\\BPROJ\\ArtVeeData\\Blue Girls (1919 - 1920) .jpg")