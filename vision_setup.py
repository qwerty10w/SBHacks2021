import io, os
import cv2 as cv
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"lookout-301909-820693edeb59.json"
client = vision.ImageAnnotatorClient()


def detect_objects(frameimg,frame):
    image = vision.Image(content=frameimg)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations

    print(localized_object_annotations)

    draw_image = frame
    height, width, channels = draw_image.shape
    for obj in localized_object_annotations:
        if(obj.name == "Person"):
            r, g, b = 255, 0 , 0
            UL = (int(obj.bounding_poly.normalized_vertices[0].x * width), int(obj.bounding_poly.normalized_vertices[0].y * height))
            LR = (int(obj.bounding_poly.normalized_vertices[2].x * width), int(obj.bounding_poly.normalized_vertices[2].y * height))
            print('args: image, {}, {}, ({}, {}, {}), 3'.format(UL, LR, r, g, b))
            cv.rectangle(draw_image, UL, LR, (b,g,r), 2)

            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(draw_image, 'Person', (int(obj.bounding_poly.normalized_vertices[0].x * width), int(obj.bounding_poly.normalized_vertices[0].y * height - 5)), font, 1, (b,g,r), lineType=cv.LINE_AA)

    ret, jpeg = cv.imencode('.jpg', draw_image)
    return jpeg.tobytes()
