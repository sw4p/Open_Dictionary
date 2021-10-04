import cv2
import re
import pytesseract
import platform
import numpy as np

# This is where tesseract is installed in my system, and yes I am using windows!
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCR:
    def identify_word(self, image, cX, cY):
        # Detect words in the cropped image
        contours = self.detect_text_blob(image)
        # Find nearest word to the marker
        minX, minY, minW, minH = self.nearest_contour(image, contours, cX, cY)
        # Bound the nearest word in a red rectangle
        cv2.rectangle(image, (minX, minY), (minX+minW, minY+minH), (0, 0, 255), 1)
        # Identify text from the red rectangle, ideally it should be only one word
        translateFrame = image[minY:minY+minH, minX:minX+minW]
        text = pytesseract.image_to_string(translateFrame)
        # Replacing every character except english alphabets with space
        word = re.sub(r'[^A-Za-z+]', '', text)

        return word

    def detect_text_blob(self, image):
        # Change color image into grayscale image
        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply binary threshold
        imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
        #cv2.imshow('Binary Image', imgBinary)

        # Apply erosion to the image
        erosionKernel = np.ones((3,3), np.uint8)
        imgEroded = cv2.erode(imgBinary, erosionKernel, iterations=3)
        cv2.imshow('Eroded Image', imgEroded)

        # Detect countours in the image
        contours, hierarchy = cv2.findContours(imgEroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image, contours, -1, (0,255,0), 1)
        #cv2.imshow('text', image)
        
        return contours

    def nearest_contour(self, image, contours, markerX, markerY):
        minDistance = np.inf
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 1)
            dist = np.sqrt((markerX-x)**2 + (markerY-y)**2)
            if dist < minDistance and w >= 50:
                minDistance = dist
                minX, minY, minW, minH = x, y, w, h
        
        if minDistance == np.inf:
            minX, minY, minW, minH = markerX, markerY, 2, 2
        
        return minX, minY, minW, minH    