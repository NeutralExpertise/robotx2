import cv2
import numpy as np

img = cv2.imread("assets/lambo.png")

# finds size of your image
print(img.shape)

# resize your image
imgResize = cv2.resize(img,(1000, 500))
print(imgResize.shape)

imgCropped = img[0:200, 200:500]

cv2.imshow("Image",img)
cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped",imgCropped)

cv2.waitKey(0)
