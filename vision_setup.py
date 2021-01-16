import io, os
# from numpy import random
from google.cloud import vision
from pillow_utility import draw_boundary, Image
# import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"lookout-301909-820693edeb59.json"
client = vision.ImageAnnotatorClient()

file_name = 'TestImage3.jpg'
image_path = os.path.join('.\Images', file_name)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations

pillow_image = Image.open(image_path)
# df = pd.DataFrame(columns=['name', 'score'])
for obj in localized_object_annotations:
    # df = df.append(
    #     dict(
    #         name=obj.name,
    #         score=obj.score
    #     ),
    #     ignore_index=True)

    # r, g, b = random.randint(150, 255), random.randint(
    #     150, 255), random.randint(150, 255)

    r, g, b = 255, 0, 0

    draw_boundary(pillow_image, obj.bounding_poly, (r, g, b),
                 pillow_image.size, obj.name, obj.score)

# print(df)
pillow_image.show()
