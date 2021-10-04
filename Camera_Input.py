import cv2
from PyDictionary import PyDictionary
import TranslatorGUI as GUI
import Marker
import Image_Source as imgSrc
import OCR

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
    ocr = OCR.OCR()

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
                word = ocr.identify_word(cropFrame, cX, cY)

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
    camera.release_source()    
    cv2.destroyAllWindows()

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
