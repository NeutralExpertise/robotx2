import cv2

img = cv2.imread("Pictures/road.jpg", -1)

cv2.imshow('Road', img)

cv2.waitKey(0)

h, w = img.shape[:2]

print("Height = {},  Width = {}".format(h, w))

(B, G, R) = img[100, 100]

print("R = {}, G = {}, B = {}".format(R, G, B))

B = img[100, 100, 0]

print("B = {}".format(B))

roi = img[100 : 500, 200 : 700]

resize = cv2.resize(img, (800, 800))

ratio = 800 / w

dim = (800, int(h * ratio))

resize_aspect = cv2.resize(img, dim)

center = (w // 2, h // 2)

matrix = cv2.getRotationMatrix2D(center, -45, 1.0)

rotated = cv2.warpAffine(img, matrix, (w, h))

output = img.copy

rectangle = cv2.rectangle(output, (1500, 900), (600, 400), (255, 0, 0), 2)

output = img.copy

text = cv2.putText(output, 'OpenCV Demo', (500,500), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 2)

cv2.imshow('Road', output)

cv2.waitKey(0)


