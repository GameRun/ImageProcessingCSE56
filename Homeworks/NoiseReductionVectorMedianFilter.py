import numpy as np
import cv2

def dist(point, wind):
    dist = 0
    for j in range (3):
        for i in range(3):
            dist = dist + np.sqrt(np.power(point[0] - wind[j,i, 0], 2) + np.power(point[1] - wind[j,i, 1], 2) + np.power(point[2] - wind[j, i,2], 2 ))

    return dist;

def vectorOperation(img):

    clearImage = np.zeros(img.shape)
    filter_size = 3
    padding_size = filter_size //2
    padding_image = np.pad(img, [(padding_size, padding_size), (padding_size, padding_size),(0,0)], mode='constant')
    for i in range(padding_image[:,0,0].shape[0]-2*padding_size) :
        for j in range(padding_image[0, :, 0].shape[0]-2*padding_size):
            print('i - j ', i,j)
            clearImage[i,j,:] = calculateMedianValue(padding_image[ i : i + filter_size , j : j + filter_size , :])


    return clearImage



def calculateMedianValue(windows):
    windowResult = {}
    for i in range(3):
        for j in range(3):
            result = dist(windows[i, j, :], windows)
            windowResult[str(i) + str(j)] = result

    sorted_dict = sorted(windowResult.items(), key=lambda x: x[1])
    return windows[ int(sorted_dict[4][0][0]), int(sorted_dict[4][0][1]), :]




def main():
    filterSize = 3

    imageName = "NoiseImage.JPG"
    image = cv2.imread('../Images/' + imageName)
    pad_Image = np.pad(image, [(3 // 2,), (filterSize // 2,), (0,)])
    result = vectorOperation(pad_Image)
    cv2.imshow(image, "orginal")
    cv2.imshow(result,"result")
    cv2.waitKey(0)

main()