from flask import Flask, render_template, Response, jsonify, request
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
update_ip = False
ip = 0


@app.route('/ip')
def get_ip():
    global update_ip, ip
    update_ip = True
    ip = request.values.get("ip")
    response = {"ip": ip}
    return jsonify(response)


@app.route('/')
def index():
    # if video_stream.get_framejpeg():
    #     return render_template('error.html')
    # else:
    return render_template('index.html')


@app.route("/auth")
def authorizer():
    global authorized, make_auth
    authorized = True
    make_auth = True
    response = {"num_authorized": "authorized"}  # n_authorized}
    return jsonify(response)


def gen(camera):
    while True:
        count = 0
        global authorized, make_auth, update_ip, ip

        if make_auth:
            framejpeg = camera.get_framejpeg()
            n_authorized = authorize(framejpeg)
            print("Authorized at {} people".format(n_authorized))

        if update_ip:
            camera.update_source(ip)
            update_ip = False
            print("Updating ip...")

        # Do not touch
        print(camera.ip)
        # Do not touch

        while authorized:
            framejpeg = camera.get_framejpeg()
            if not framejpeg:
                continue

            frame = camera.get_frame()

            if(count % 10 == 0):
                framejpeg, intruder = detect_objects(framejpeg, frame, n_authorized)

            if(count == 100):
                count = 0

            count += 1

            if intruder:
                meme()
                authorized = False
                make_auth = False

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + framejpeg + b'\r\n\r\n')

        framejpeg = camera.get_framejpeg()
        if not framejpeg:
            continue

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + framejpeg + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
