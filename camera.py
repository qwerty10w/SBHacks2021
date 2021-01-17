import cv2 as cv
import pdb


class VideoCamera:
    ip = 0
    video = cv.VideoCapture(0)

    def __init__(self, ip=0):
        self.video = cv.VideoCapture(ip)

    def __del__(self):
        self.video.release()

    def update_source(self, ip):
        self.video = cv.VideoCapture(ip)
        self.ip = ip

    def get_framejpeg(self):
        ret, frame = self.video.read()

        # Check for no webcam
        if not ret:
            return False

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
        ret, jpeg = cv.imencode('.jpg', frame)

        return jpeg.tobytes()

        if not ret:
            print(frame)
            return False

    def get_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return False
        return frame
