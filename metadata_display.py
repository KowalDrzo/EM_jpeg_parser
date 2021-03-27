import os
from PIL import Image
from PIL.ExifTags import TAGS

img_file = "benek2.jpg"
img = Image.open(img_file)

exif_data = img.getexif()

for tagId in exif_data:
    tag = TAGS.get(tagId, tagId)
    data = exif_data.get(tagId)
    print(f"{tag:16}: {data}")

