import pywt
import cv2

def run(filepath):
    img     = cv2.imread(filepath)
    coeffs2 = pywt.dwt2(img, "haar")
    
    LL, (LH, HL, HH) = coeffs2

    ll = round(LL.mean(), 3)
    l2 = round(pywt.idwt2(coeffs2, "haar").mean(), 3)

    return ll, l2