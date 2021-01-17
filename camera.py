import cv2 as cv


class VideoCamera:
    def __init__(self, ip=0):
        self.video = cv.VideoCapture('https://192.168.86.52:8080/video')
        # https://10.0.0.206:8080/video ANDY
        # https://192.168.86.52:8080/video NEIL

    def __del__(self):
        self.video.release()

    def get_framejpeg(self):
        ret, frame = self.video.read()

        # Check for no webcam
        # if not ret:
        #     return False

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
        ret, jpeg = cv.imencode('.jpg', frame)

        return jpeg.tobytes()

        if not ret:
            print(frame)
            return False

    def get_frame(self):
        ret, frame = self.video.read()
        return frame
