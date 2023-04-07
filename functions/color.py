import cv2


def run(filepath):
    img     = cv2.imread(filepath)

    r = 0
    g = 0
    b = 0

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j][0] >= 125:
                r += 1
            if img[i][j][1] >= 125:
                g += 1
            if img[i][j][2] >= 125:
                b += 1

    return r, g, b