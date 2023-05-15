import cv2
from skimage.feature import graycomatrix

def run(filepath):
    img     = cv2.imread(filepath)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    glcm       = graycomatrix(gray, 
                              distances=[5], 
                              angles=[0], 
                              levels=256,
                              symmetric=True, 
                              normed=True).mean()
    
    return glcm