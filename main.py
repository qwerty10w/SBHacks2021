from flask import Flask, render_template, Response, jsonify
from camera import VideoCamera
from vision_setup import detect_objects, authorize
from rickroll import meme
import pdb


app = Flask(__name__)

# with open('ip.txt', 'r') as file:
#     data = file.read()

video_stream = VideoCamera()
authorized = False
make_auth = False


@app.route('/')
def index():
    # if video_stream.get_framejpeg():
    #     return render_template('error.html')
    # else:
    return render_template('index.html')


@app.route("/auth")
def authorizer():
    global authorized
    authorized = True
    global make_auth
    make_auth = True
    response = {"num_authorized": "authorized"}  # n_authorized}
    return jsonify(response)


def gen(camera):
    while True:
        count = 0
        global authorized
        global make_auth
        if make_auth:
            framejpeg = camera.get_framejpeg()
            n_authorized = authorize(framejpeg)
            print("authorized at {} people".format(n_authorized))

        while authorized:
            framejpeg = camera.get_framejpeg()
            frame = camera.get_frame()

            if(count % 10 == 0):
                # global n_authorized
                framejpeg, intruder, num = detect_objects(framejpeg, frame, n_authorized)
                print(num, intruder)

            if(count == 100):
                count = 0

            count += 1

            if intruder:
                meme()
                authorized = False
                make_auth = False

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + framejpeg + b'\r\n\r\n')

        framejpeg = camera.get_framejpeg()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + framejpeg + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
