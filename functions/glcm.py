import cv2
from skimage.feature import graycomatrix

def run(filepath):
    img     = cv2.imread(filepath)

    glcm       = graycomatrix(img[:, :, 1], 
                              distances=[5], 
                              angles=[0], 
                              levels=256,
                              symmetric=True, 
                              normed=True).mean()
    
    return glcm