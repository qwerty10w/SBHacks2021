import cv2

class VideoCamera:
    def __init__(self, ip=0):
        self.video = cv2.VideoCapture('http://192.168.86.52:8080/video')

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
