import os
import cv2
import pywt
from sklearn.neighbors import KNeighborsClassifier

def extract_wavelet(filepath):
    img     = cv2.imread(filepath)
    coeffs2 = pywt.dwt2(img, "haar")
    
    LL, (LH, HL, HH) = coeffs2

    return LL.mean(), HL.mean()


def getListOfFiles(dirName:str) -> list:
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def run(imgpath):
    imagePaths = getListOfFiles("./datasets/")
    x = []
    y = []
    classes = []

    label = os.listdir("./datasets/")

    for image in imagePaths:
        label_target = [os.path.split(os.path.split(image)[0])[1]]
        LL, HL = extract_wavelet(image)

        x.append(LL)
        y.append(HL)
        
        res = [label.index(i) for i in label_target]
        classes.append(res)

    data = list(zip(x, y))
    knn = KNeighborsClassifier(n_neighbors=4)

    knn.fit(data, classes)

    imgtest = extract_wavelet(imgpath)

    predict_true = 0
    for i, _ in enumerate(classes):
        result = knn.predict([(x[i], y[i])])
        if result == classes[i]:
            predict_true += 1

    accuracy = (predict_true/(len(classes)))*100

    return label[knn.predict([imgtest])[0]], accuracy
