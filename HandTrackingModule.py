import cv2
import mediapipe as mp
import time
import numpy as np


class handDetector:

    def __init__(self, mode=False, maxHands=2,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.results = None      # <-- Added (avoids AttributeError)
        self.lmList = []
        self.tipIds = [4,8,12,16,20]
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS
                    )

        return img

    def findPosition(self, img, handNo=0, draw=True):

        xList = []
        yList = []
        bbox = []
        lmList = []

        if self.results is None:
            return lmList, bbox

        if self.results.multi_hand_landmarks:

            if handNo >= len(self.results.multi_hand_landmarks):
                return lmList, bbox

            myHand = self.results.multi_hand_landmarks[handNo]

            h, w, c = img.shape

            for id, lm in enumerate(myHand.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                xList.append(cx)
                yList.append(cy)

                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)

            bbox = (xmin, ymin, xmax, ymax)

            if draw:
                cv2.rectangle(img,
                            (xmin - 20, ymin - 20),
                            (xmax + 20, ymax + 20),
                            (0, 255, 0),
                            2)
        self.lmList = lmList
        return lmList, bbox
    def fingersUp(self):

       

        print("Inside fingersUp")

        fingers = []

        if not hasattr(self, "lmList"):
            print("lmList not found")
            return fingers

        if len(self.lmList) == 0:
            print("lmList empty")
            return fingers

        print("lmList length =", len(self.lmList))

        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    def findDistance(self, p1, p2, img, draw=True):

        if len(self.lmList) == 0:
            return 0, img, []

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = np.hypot(x2 - x1, y2 - y1)

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

            

        return length, img, [x1, y1, x2, y2, cx, cy]
    def box(self, img, draw=True):
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                x_min = min([lm.x for lm in handLms.landmark])
                x_max = max([lm.x for lm in handLms.landmark])
                y_min = min([lm.y for lm in handLms.landmark])
                y_max = max([lm.y for lm in handLms.landmark])

                h, w, c = img.shape
                x_min, x_max = int(x_min * w), int(x_max * w)
                y_min, y_max = int(y_min * h), int(y_max * h)

                if draw:
                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        return img
def main():

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:

        success, img = cap.read()

        if not success:
            break

        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])  # Thumb tip coordinates

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()