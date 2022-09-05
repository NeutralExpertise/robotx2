import cv2

# load an image
img = cv2.imread('resources/red-buoy.jpg', -1)
# resizes image.  Parameters are (image, dimensionA:400, dimensionb:400))
imgResize = cv2.resize(img, (400,400))
imgResize2 = cv2.resize(img, (400,400), fx=0.5, fy=2)
# rotates image
imgRotate = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


# displays image(s)
cv2.imshow("Red-Bouy", img)
cv2.imshow("Red-Bouy-Resize", imgResize)
cv2.imshow("Red-Bouy-CounterClockWise", imgRotate)

# write to new file after image manipulation
cv2.imwrite("new_red_buoy.jpg", imgRotate)

# wait infinately to destroy all windows
cv2.waitKey(0)
cv2.destroyAllWindows()

