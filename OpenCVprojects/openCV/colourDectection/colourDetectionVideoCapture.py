import cv2


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width/2)
    cy = int(height/2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    colour = "undefined"
    if hue_value < 5:
        colour = "RED"
    elif hue_value < 22:
        colour = "ORANGE"
    elif hue_value < 33:
        colour = "YELLOW"
    elif hue_value < 78:
        colour = "GREEN"
    elif hue_value < 131:
        colour = "BLUE"
    elif hue_value < 170:
        colour = "VIOLET"
    else:
        colour = "RED"

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.putText(frame, colour, (10, 70), 0, 1.5, (b, g, r), 2)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)


    cv2.imshow("FrameCapture", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()