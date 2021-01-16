from flask import Flask, render_template, Response
from camera import VideoCamera
from vision_setup import detect_objects
import cv2

app = Flask(__name__)

with open('ip.txt', 'r') as file:
    data = file.read()

video_stream = VideoCamera(data)

@app.route('/')
def index():
    if video_stream.get_framejpeg() == False:
        return render_template('error.html')
    else:
        return render_template('index.html')
 
def gen(camera):
    while True:
        framejpeg = camera.get_framejpeg()
        frame = camera.get_frame()
<<<<<<< HEAD
        
        edited_frame = detect_objects(framejpeg, frame)
        
=======
        if framejpeg == False:
            return render_template('error.html')
        
        edited_frame = detect_objects(framejpeg, frame)
        

>>>>>>> ab6719ac953fd18d482a419c2d879f26c427639f
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + edited_frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream),
        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)