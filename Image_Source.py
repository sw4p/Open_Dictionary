import cv2

class ImageSource():
    def __init__(self, source="webCam", cameraIndex=0):
        self.source = source
        if self.source == "webCam":
            self.camera = cv2.VideoCapture(cameraIndex, cv2.CAP_DSHOW)
        elif self.source == "piCam":
            from picamera import PiCamera
            from picamera.array import PiRGBArray
            
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 30
            self.camera.vflip = True
            self.camera.hflip = True
            self.rawCapture = PiRGBArray(self.camera, size=(640, 480))


    def frame(self):
        if self.source == "piCam":
            self.rawCapture.truncate(0)
            self.camera.capture(self.rawCapture, format='bgr', use_video_port=True)
            image = self.rawCapture.array
        elif self.source == "webCam":
            ret, image = self.camera.read()

        return image

    def releaseSource(self):
        if self.source == "webCam":
            self.camera.release()

#ImageInput()