import io
import os
import cv2 as cv
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"lookout-301909-820693edeb59.json"
client = vision.ImageAnnotatorClient()


def detect_objects(frameimg, frame, num_authorized):
    image = vision.Image(content=frameimg)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations

    intruder = False

    draw_image = frame
    height, width, channels = draw_image.shape
    num_present = 0
    for obj in localized_object_annotations:
        if(obj.name == "Person"):
            num_present += 1

            r, g, b = 255, 0, 0
            UL = (int(obj.bounding_poly.normalized_vertices[0].x * width),
                  int(obj.bounding_poly.normalized_vertices[0].y * height))
            LR = (int(obj.bounding_poly.normalized_vertices[2].x * width),
                  int(obj.bounding_poly.normalized_vertices[2].y * height))

            cv.rectangle(draw_image, UL, LR, (b, g, r), 2)

            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(draw_image, 'Person', (int(obj.bounding_poly.normalized_vertices[0].x * width), int(
                obj.bounding_poly.normalized_vertices[0].y * height - 5)), font, 1, (b, g, r), lineType=cv.LINE_AA)

            # Detect Action Cases
            if(num_present > num_authorized):
                print("Intruder detected, seting intruder flag to 1...")
                intruder = True
            elif(num_present == 0):
                print("Client left seting intruder flag to 1...")
                intruder = True

    ret, jpeg = cv.imencode('.jpg', draw_image)
    return jpeg.tobytes(), intruder, num_present


# @app.route("/authorize")
def authorize(frameimg):
    image = vision.Image(content=frameimg)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations

    num_authorized = 0

    for obj in localized_object_annotations:
        if(obj.name == "Person"):
            num_authorized += 1

    return num_authorized
