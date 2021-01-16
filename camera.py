import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()        

    def get_framejpeg(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
        try:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        except:
            return False

    def get_frame(self):
        ret, frame = self.video.read()
        return frame