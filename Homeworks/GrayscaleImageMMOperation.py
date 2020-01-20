import cv2
import numpy as np
image = cv2.imread('../Images/eye.png', cv2.IMREAD_GRAYSCALE)


kernel = np.ones((23,23), np.uint8)
img_erosion = cv2.erode(image, kernel, iterations=1)
img_dilation = cv2.dilate(image, kernel, iterations=1)
k =  image-img_erosion

opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
cv2.morphologyEx(image, cv2.M)

cv2.imshow('Input', image)
cv2.imshow('Erosion', img_erosion)
cv2.imshow('Dilation', img_dilation)
cv2.imshow('Opening', opening)
cv2.imshow('Closing', closing)
cv2.waitKey(0)
