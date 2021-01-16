from flask import Flask, render_template, Response
from camera import VideoCamera
from vision_setup import detect_objects
import cv2

app = Flask(__name__)

video_stream = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')
 
def gen(camera):
    while True:
        framejpeg = camera.get_framejpeg()
        frame = camera.get_frame()
        if framejpeg == False:
            return render_template('error.html')
        
        edited_frame = detect_objects(framejpeg, frame)
        

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + edited_frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream),
        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)