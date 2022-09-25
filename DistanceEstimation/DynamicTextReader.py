import cv2
import cvzone

from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

textList = ["All Hail King Charles", "Third of his Name", "King of the Andals and First Men",
            "Lord of the United Kingdoms", "and Protector of the Commonwealth"]

sen = 20

while True:
    ret, frame = cap.read()
    frameText = np.zeros_like(frame)
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3

        # Finding distance
        f = 840
        d = (W * f) / w
        print(d)

        cvzone.putTextRect(frame, f'Depth: {int(d)}cm', (face[10][0] - 100, face[10][1] - 50), scale=2)
        for i, text in enumerate(textList):
            singleHeight = 20 + int((int(d/sen)*sen)/4)
            scale = 0.4 + (int(d/sen)*sen)/75
            cv2.putText(frameText, text, (50, 50+(i*singleHeight)), cv2.FONT_ITALIC, scale, (255, 255, 255), 2)

    frameStacked = cvzone.stackImages([frame, frameText], 2, 1)

    cv2.imshow("Frame", frameStacked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
