import cv2
import numpy as np
import pytesseract
from PyDictionary import PyDictionary
import TranslatorGUI as GUI
import Marker
import Image_Source as imgSrc
import platform
import re

# This is where tesseract is installed in my system, and yes I am using windows!
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def main():
    # Box of interest coordinates
    x1 = 100
    y1 = 100
    w = 150
    h = 80

    # Objects
    gui = GUI.Translator_GUI()
    marker = Marker.Marker()
    camera = imgSrc.ImageSource(source="piCam")
    dictionary = PyDictionary()

    while (True):
        # Capture image frame
        frame = camera.frame()
        
        # Identify maker position from the image
        cX, cY = marker.colour(frame, [0,-10], displayMask=False)
        if cX != -1:
            # Draw white dot at the center of the marker
            cv2.circle(frame, (cX, cY), 2, (255, 255, 255), -1)

            startPoint = (int(cX-w/2), cY-h)
            endPoint = (int(cX+w/2), cY)
            cv2.rectangle(frame, startPoint, endPoint, (0,255,0), 1)
            # Crop image around area of interest
            cropFrame = frame[startPoint[1]:endPoint[1], startPoint[0]:endPoint[0]]
            if cropFrame.any():
                # Detect words in the cropped image
                contours = Detect_Text_Blob(cropFrame)
                # Find nearest word to the marker
                minX, minY, minW, minH = Nearest_Contour(cropFrame, contours, cX, cY)
                # Bound the nearest word in a red rectangle
                cv2.rectangle(cropFrame, (minX, minY), (minX+minW, minY+minH), (0, 0, 255), 1)
                # Identify text from the red rectangle, ideally it should be only one word
                translateFrame = cropFrame[minY:minY+minH, minX:minX+minW]
                text = pytesseract.image_to_string(translateFrame)
                # Replacing every character except english alphabets with space
                word = re.sub(r'[^A-Za-z+]', '', text)

                if word != '':
                    print(word)
                    meaning = dictionary.meaning(word)
                    noun, verb, adj = Extract_Information(meaning)
                    gui.update(word, noun, verb, adj)

        # Display image
        cv2.imshow('frame', frame)
        #cv2.imshow('cropFrame', cropFrame)
        #cv2.imshow('translateFrame', translateFrame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera and destroy everything
    camera.releaseSource()    
    cv2.destroyAllWindows()
    
def Detect_Text_Blob(image):
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

def Nearest_Contour(image, contours, markerX, markerY):
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

def Extract_Information(meaning):
    Noun, Verb, Adjective = "None", "None", "None"
    if meaning != None:
        for key in meaning.keys():
            if key == "Noun":
                Noun = meaning[key][0]#'\n'.join(meaning[key])
            elif key == "Verb":
                Verb = meaning[key][0]#'\n'.join(meaning[key])
            elif key == "Adjective":
                Adjective = meaning[key][0]#'\n'.join(meaning[key])

    return Noun, Verb, Adjective


# Call main function
main()
