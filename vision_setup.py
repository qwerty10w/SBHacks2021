import io, os
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"lookout-301909-820693edeb59.json"
client = vision.ImageAnnotatorClient()


def detect_objects(frameimg):

    image = vision.Image(content=frameimg)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations

    print(localized_object_annotations)

