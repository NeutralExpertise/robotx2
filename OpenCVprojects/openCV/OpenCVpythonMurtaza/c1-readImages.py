import cv2

# LOAD AN IMAGE USING 'IMREAD'
img = cv2.imread("assets/lena.png", -1)
# DISPLAY
cv2.imshow("Lena Soderberg", img)
cv2.waitKey(0)


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture("assets/test_ video.mp4")
while True:
    success, img = cap.read()
    img = cv2.resize(img, (frameWidth, frameHeight))
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break