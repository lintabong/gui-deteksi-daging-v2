import cv2


def run(filepath):
    img     = cv2.imread(filepath)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue     = img_hsv[:, : ,0].mean()

    saturation = img_hsv[:, :, 1].mean()

    return hue, saturation