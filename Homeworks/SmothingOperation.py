import numpy as np
import cv2
from PIL import Image
import math

mean_smothing_rate = 1/9
gaus_smothing_Rate = 1/273

def createMeanSmothingFilter(size):
    return np.ones([size,size]) / (size*size)


def smothingOperation(image, kernel):
    padding_size = kernel.shape[0] //2
    result = np.zeros([image.shape[0] - padding_size , image.shape[1] - padding_size ])
    for i in range(padding_size,image.shape[0] - padding_size):
        for j in range(padding_size, image.shape[1] - padding_size):
            print('i, j', i, j)
            result[i,j] =np.sum ( (image[ (i -padding_size) : (i + kernel.shape[0]-padding_size) , (j - padding_size)  : (j + kernel.shape[0]-padding_size)]* (kernel)) )
            print('i, j', i, j, result[i,j])

    return result

def meanSmothingTest():
    image = cv2.imread('../Images/edison.jpg', cv2.IMREAD_GRAYSCALE)
    filterSize = 3
    kernel = createMeanSmothingFilter(filterSize)
    pad_Image = np.pad(image, [(filterSize//2 ,  ),(filterSize//2 ,)])
    smothedImage = smothingOperation(pad_Image, kernel)

    img = Image.fromarray(smothedImage)
    img.show(title = "Smothed")

    img2= Image.fromarray(image)
    img2.show(title = "Smothed")

meanSmothingTest()

def createGaussSmothingFilter(filterSize, sigma):
    radius = (filterSize // 2)

    k = np.arange(2*radius +1)
    row = np.exp( -(((k - radius)/(sigma))**2)/2.)
    col = row.transpose()
    out = np.outer(row, col)
    out = out/np.sum(out)
    return out



def gaussSmothingTest():
    image = cv2.imread('../Images/edison.jpg', cv2.IMREAD_GRAYSCALE)
    filterSize = 5
    sigma = 1
    kernel = createGaussSmothingFilter(filterSize, sigma)
    pad_Image = np.pad(image, [(filterSize//2 ,  ),(filterSize//2 ,)])
    smothedImage = smothingOperation(pad_Image, kernel)

    img = Image.fromarray(smothedImage)
    img.show(title = "Smothed")

    img2= Image.fromarray(image)
    img2.show(title = "Smothed")


gaussSmothingTest()