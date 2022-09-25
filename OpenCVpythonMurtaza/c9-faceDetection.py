import cv2

# add Cascade - cascades detect different things such as number plates, eyes, full body, etc
faceCascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")

# import lena image from assets folder
img = cv2.imread('assets/lena.png')

# convert image to grayscale
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# find face in lena image using face Cascade.  Parameters are (image, scalefactor(1,1), minimum_neigbours(4))
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

# create bounding box around the faces detected
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y), (x+w,y+h), (255,0,0),2)

# display image using imshow function
cv2.imshow("Result", img)
cv2.waitKey(0)