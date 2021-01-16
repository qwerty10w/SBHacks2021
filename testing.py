import io, os
import cv2 as cv
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"lookout-301909-820693edeb59.json"
client = vision.ImageAnnotatorClient()

file_name = 'TestImage2.jpg'
image_path = os.path.join('.\Images', file_name)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    print(localized_object_annotations)

    draw_image = cv.imread(image_path)
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

    cv.imshow('image', draw_image)
    k = cv.waitKey(0) & 0xFF
    if(k == 27):
        cv.destroyAllWindows()
