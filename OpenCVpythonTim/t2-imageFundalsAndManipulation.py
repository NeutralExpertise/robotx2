import cv2
import random
# load an image
img = cv2.imread('resources/red-buoy.jpg', -1)

# images are represented in numpy arrays, numpy is a high performance array library for python
print(img.shape) # (675 = height/rows, 900 = width/columns, 3 = channels)


print(img[257][400])

# change first 100 rows to random pixel
for i in range(100):
    for j in range(img.shape[1]):
        img[i][j] = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

# copy one part (slice) of an image and paste it in another part of the image
# copies rows from 500-700, then copies columns from 600-900 from the rows
tag = img[100:300, 600:900]

# paste into an area of the array, must be same dimensions
img[50:250, 20:320] = tag


cv2.imshow('Image', img)
cv2.imshow('ImageTag', tag)
cv2.waitKey(0)
cv2.destroyAllWindows()

