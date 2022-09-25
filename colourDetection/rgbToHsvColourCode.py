# Python programs to find
# unique HSV code for color

# Importing the libraries openCV & numpy
import cv2
import numpy as np

# Get green color
white = np.uint8([[[255, 255, 0]]])

# Convert Green color to Green HSV
hsv_white = cv2.cvtColor(white, cv2.COLOR_BGR2HSV)

# Print HSV Value for Green color
print(hsv_white)

# Make python sleep for unlimited time
cv2.waitKey(0)