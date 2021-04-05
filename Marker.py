import cv2
import mediapipe as mp
import numpy as np

class Marker:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def colour(self, image, offsets=[0,0], displayMask=False):
        # Conver BGR to HSV
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Detect red colour. Red colour has two range in HSV, 0-30 and 150-180.
        # here we are detecting only extreme red i.e. 0-10 and 170-180.
        colourBoundry = ([0, 120, 70], [10, 255, 255]) #HSV
        mask1 = self.Identify_Colour(image, colourBoundry)
        colourBoundry = ([170, 120, 70], [180, 255, 255]) #HSV
        mask2 = self.Identify_Colour(image, colourBoundry)
        # ORing the masks
        mask1 = mask1 + mask2
        # Display mask
        if displayMask != False:
            cv2.imshow('mask', mask1)

        # Calculate center of the coloured blob
        M = cv2.moments(mask1)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"]) + offsets[0]
            cY = int(M["m01"] / M["m00"]) + offsets[1]
        else:
            cX, cY = -1, -1

        return cX, cY

    def finger(self, image, offsets=[0,0]):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(image, handLms)

        cv2.imshow("finger", image)

    def Identify_Colour(self, image, colourBoundry):
        lower = np.array(colourBoundry[0], dtype="uint8")
        upper = np.array(colourBoundry[1], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)
        return mask