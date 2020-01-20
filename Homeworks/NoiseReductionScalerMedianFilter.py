import numpy as np
import cv2


def scalerMedianFilter(image, kernel_size):
    padding_size = kernel_size //2
    result = np.zeros([image.shape[0] - 2*padding_size , image.shape[1] - 2*padding_size ,3])
    for c in range(image.shape[2]):
        for i in range(0,image.shape[0] - 2*padding_size):
            for j in range(0, image.shape[1] - 2*padding_size):

                result[i,j,c] =int(np.median(image[ (i ) : (i + kernel_size) , (j )  : (j + kernel_size),c]))

    return result


def main():
    filterSize = 3
    imageName ="NoiseImage.JPG"
    image = cv2.imread('../Images/'+imageName)
    pad_Image = np.pad(image, [(3 // 2,), (filterSize // 2,), (0,)])
    result = scalerMedianFilter(pad_Image, filterSize)
    cv2.imshow(image, "orginal")
    cv2.imshow(result,"result")
    cv2.waitKey(0)

main()

