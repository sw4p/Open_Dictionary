import cv2
import numpy as np
import pytesseract
from googletrans import Translator
from PyDictionary import PyDictionary
import re

pi = True

if pi == True:
    from picamera import PiCamera
    from picamera.array import PiRGBArray

dictionary = PyDictionary()
#translator = Translator()

# This is where tesseract is installed in my system, and yes I am using windows!
if pi == False:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def main():
    if pi == True:
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.hflip = 1
        camera.vflip = 1
        rawCapture = PiRGBArray(camera, size=(640, 480))
    else:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Box of interest coordinates/
    x1 = 100
    y1 = 100
    w = 150
    h = 50

    #while (True):
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        # Capture image frame
        if pi == True:
            frame = frame.array
        else:
            ret, frame = cap.read()
        
        # Identify maker position from the image
        cX, cY = Idenfity_Marker(frame, displayMask=False)
        # Draw white dot at the center of the marker
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

        # Draw a rectange in green color i.e. box of interest around captured image
        #cv2.rectangle(frame, (x1,y1), (x1+w,y1+h), (0,255,0), 2)
        startPoint = (int(cX-w/2), cY-h)
        endPoint = (int(cX+w/2), cY)
        cv2.rectangle(frame, startPoint, endPoint, (0,255,0), 2)
        # Crop image around box of interest
        translateFrame = frame[startPoint[1]:endPoint[1], startPoint[0]:endPoint[0]]

        # Detect text as a blob from the image
        contours = Detect_Text_Blob(translateFrame)
        # Find nearest contour to the marker
        minX, minY, minW, minH = Nearest_Contour(contours, cX, cY)
        cv2.rectangle(translateFrame, (minX, minY), (minX+minW, minY+minH), (255, 0, 0), 1)

        # Identify text from image
        #data = pytesseract.image_to_string(translationFrame, output_type='dict')
        text = pytesseract.image_to_string(translateFrame)
        #print(text)
        # Replacing every character except english alphabets with ''
        text = re.sub(r'[^A-Za-z' ']', '', text)

        if text != '':
            print(text)
            #print(dictionary.meaning(text))
            #print(dictionary.synonym(text))
    
        #print(translator.translate(data).pronunciation)

        # Display image
        cv2.imshow('frame', frame)
        cv2.imshow('frame1', translateFrame)
        if pi == True:
            rawCapture.truncate(0)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera and destroy everything
    if pi == False:
        cap.release()
    
    cv2.destroyAllWindows()

def Idenfity_Marker(image, displayMask=False):
    # Conver BGR to HSV
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Detect red colour. Red colour has two range in HSV, 0-30 and 150-180.
    # here we are detecting only extreme red i.e. 0-10 and 170-180.
    colourBoundry = ([0, 120, 70], [10, 255, 255]) #HSV
    mask1 = Identify_Colour(image, colourBoundry)
    colourBoundry = ([170, 120, 70], [180, 255, 255]) #HSV
    mask2 = Identify_Colour(image, colourBoundry)
    # ORing the masks
    mask1 = mask1 + mask2
    # Display mask
    if displayMask != False:
        cv2.imshow('mask', mask1)

    # Calculate center of the coloured blob
    M = cv2.moments(mask1)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    return cX, cY

def Identify_Colour(image, colourBoundry):
    lower = np.array(colourBoundry[0], dtype="uint8")
    upper = np.array(colourBoundry[1], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    return mask
    
def Detect_Text_Blob(image):
    # Change color image into grayscale image
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary threshold
    imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
    #cv2.imshow('Binary Image', imgBinary)

    # Apply erosion to the image
    erosionKernel = np.ones((3,3), np.uint8)
    imgEroded = cv2.erode(imgBinary, erosionKernel, iterations=1)
    cv2.imshow('Eroded Image', imgEroded)

    # Detect countours in the image
    contours, hierarchy = cv2.findContours(imgEroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image, contours, -1, (0,255,0), 1)
    #cv2.imshow('text', image)
    
    return contours

def Nearest_Contour(contours, markerX, markerY):
    minDistance = np.inf
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        dist = np.sqrt((markerX-x)**2 + (markerY-y)**2)
        if dist < minDistance:
            minDistance = dist
            minX, minY, minW, minH = x, y, w, h
    
    return minX, minY, minW, minH

# Call main function
main()
