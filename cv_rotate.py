import cv2
import numpy as np
import random
from io import StringIO
from io import BytesIO
from PIL import Image

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

img = cv2.imread('./data/test.jpeg')
img = cv2.resize(img, (600, 600))



rotate_img = rotate_image(img, 0)

image = Image.fromarray(cv2.cvtColor(rotate_img, cv2.COLOR_BGR2RGB))
buffer = BytesIO()
image.save(buffer, "JPEG", quality=30)
jpeg_image = Image.open(buffer)
jpeg_image = cv2.cvtColor(np.asarray(jpeg_image),cv2.COLOR_RGB2BGR) 


# rotate_img = rotate_img.transpose((1,0,2))
# print(rotate_img.shape)

# cv2.imshow('origin_img', img)
cv2.imshow('rotate_img', rotate_img)
cv2.imshow('rotatejpeg_image_img', jpeg_image)
cv2.waitKey(-1)