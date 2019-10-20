import numpy as np
import utilty.Filter as f
import cv2


def prepareSubMatrixPoint(i, j, height, width, rawImage):

    if i - height // 2 < 0 :
        xi = 0
    else:
        xi = i - height // 2

    if j - width // 2 < 0 :
        yi = 0
    else:
        yi = j - width // 2

    if i + height //2 > rawImage.shape[0]:
        xn = rawImage.shape[0]
    else:
        xn = i + height //2 + 1

    if j + width //2 > rawImage.shape[1]:
        yn = rawImage.shape[1]
    else:
        yn = j + width //2 + 1

    return xi, yi, xn, yn


def dilation(rawImage, width, height, borderSize, filterType):

    processedImage = np.zeros(rawImage.shape)
    filter = f.createFilter(filterType, height, width )
    for i in range(1 , processedImage[:,0].size - borderSize):
        for j in range(1 , processedImage[0,:].size - borderSize):
            if rawImage[i,j] == 1 :
                xi, yi, xn, yn = prepareSubMatrixPoint(i,j, height, width, rawImage)
               # indisler başlangıç ve bitişten büyükmü diye kontrol edilmeli bunun içinde metod yazıcam boyları orada handle etmesi gerekiyor.
                processedImage[xi : xn, yi: yn ] = matrisOr(processedImage[xi : xn, yi: yn ], filter)

    return processedImage

def erosion(rawImage, height, width, borderSize, filterType):
    processedImage = np.zeros(rawImage.shape)
    filter = f.createFilter(filterType, height, width)
    for i in range(1 , processedImage[:,0].size - borderSize):
        for j in range(1 , processedImage[0,:].size - borderSize):
            xi, yi, xn, yn = prepareSubMatrixPoint(i, j, height, width, rawImage)
            if  isEqualSubImageWithFilter(rawImage[xi : xn, yi: yn], filter) :#burası daha iyi olabilir np.array_equal(rawImage[xi : xn, yi: yn] , filter) zaten 1 mi diye kontrol ediyoruz
                processedImage[i , j] = 1
    return processedImage


def opening(rawImage, height , width , borderSize, filterType):

    erosionImage = erosion(rawImage, height , width , borderSize, filterType)

    processedImage = dilation(erosionImage , height , width , borderSize, filterType)

    return processedImage


def closing(rawImage, height , width , borderSize, filterType):

    dilationImage = dilation(rawImage , height , width , borderSize, filterType)

    processedImage = erosion(dilationImage, height , width , borderSize, filterType)

    return processedImage

def isEqualSubImageWithFilter(image, filter):
    for i in range(filter[0].size):
        for j in range(filter[0].size):
            if filter[i,j] == 1:
                if not filter[i,j] == image[i,j]:
                    return False

    return True

def addBorder(borderSize, grayscale_image):
    a_border = np.zeros([grayscale_image.shape[0] + (2 * borderSize), grayscale_image.shape[1] + (2 * borderSize)])
    a_border[1:grayscale_image.shape[0] + 1, 1:grayscale_image.shape[1] + 1] = grayscale_image
    return a_border


def matrisOr(image, diloded):
    bool_image = image==1
    bool_diloded =  diloded ==1
    return np.bitwise_or(bool_image, bool_diloded)* 1.0

def matrisAnd(image, diloded):
    bool_image = image==1
    bool_diloded =  diloded ==1
    return np.bitwise_and(bool_image, bool_diloded)* 1.0

def gearDefectDetect():
    image = cv2.imread('../Images/gears.png', cv2.IMREAD_GRAYSCALE)
    raw_image = image // 255

    filterSize = 111
    borderSize = filterSize // 2



    image = addBorder(borderSize, raw_image)
    cv2.imshow("orjinal image", image[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)

    filterType = "hole_circle"
    print("erosion")
    varStepOne = erosion(image, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("Erosion", varStepOne[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)

    filterType = "fill_circle"
    print("dilation")
    varStepTwo = dilation(varStepOne, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("Dilation", varStepTwo[1:raw_image.shape[0] + borderSize, 1: raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)

    varStepThree = matrisOr(image, varStepTwo)

    print("imageSum")
    cv2.imshow("ImageOrDilationImage", varStepThree[1:raw_image.shape[0] + borderSize, 1: raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)


    filterSize = 21
    borderSize = filterSize // 2
    filterType = "fill_circle"
    #ErosionWithCircle = addBorder(borderSize, varStepThree)
    varStepFour = erosion(varStepThree, filterSize, filterSize, borderSize , filterType)
    cv2.imshow("ErosionWithCircle", varStepFour[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)


    varStepFive = dilation(varStepFour, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("dilotion", varStepFive[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)
    print("2222")

    filterSize = 17
    borderSize = filterSize // 2
    varStepSix = dilation(varStepFive, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("dilotionOpening", varStepSix[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)
    print("3333")
    filterSize = 11
    borderSize = filterSize // 2
    varStepSeven = dilation(varStepSix, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("dilotionImage", varStepSeven[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)
    print("444")
    varStepEight = varStepSeven - varStepSix
    print("555")
    cv2.imshow("subtract", varStepEight[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)
    filterSize = 11
    borderSize = filterSize // 2
    varStepNine = dilation(varStepEight, filterSize, filterSize, borderSize, filterType)

    varStepTen = matrisAnd(image, varStepNine)
    print("666")
    cv2.imshow("andImage", varStepTen[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)

    filterSize = 17
    borderSize = filterSize // 2
    print("777")
    varStepEleven = dilation(varStepTen, filterSize, filterSize, borderSize, filterType)

    cv2.imshow("andImageDilation", varStepEleven[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)
    filterSize = 13
    borderSize = filterSize // 2
    subtractNew = dilation(varStepEight, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("subtractDilation", subtractNew[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])

    print("888")
    result = subtractNew - varStepEleven
    cv2.imshow("result", result[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey(1000)

    filterSize = 11
    borderSize = filterSize // 2

    print("999")
    result = subtractNew - varStepEleven
    resultEroded = erosion(result, filterSize, filterSize, borderSize, filterType)
    cv2.imshow("result", resultEroded[1:raw_image.shape[0] + borderSize, 1:raw_image.shape[1] + borderSize])
    cv2.waitKey()


gearDefectDetect()