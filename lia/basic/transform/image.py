import base64

import cv2


def to_base64(image):
    base64_img = cv2.imencode(".png", image)[1]
    base64_img = base64.b64encode(base64_img).decode("utf-8")
    return base64_img
