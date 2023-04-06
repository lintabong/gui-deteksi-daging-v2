from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import  train_test_split
import os
import cv2
import numpy as np


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
    data   = []
    lables = []

    label = ["Daging Babi", "Daging Kambing", "Daging Kerbau", "Daging Kuda", "Daging Sapi"]

    for image in imagePaths:

        lable = os.path.split(os.path.split(image)[0])[1]
        lables.append(lable)

        img = cv2.imread(image)
        img = cv2.resize(img, (32, 32), interpolation = cv2.INTER_AREA)
        data.append(img)
        
    data = np.array(data)
    lables = np.array(lables)

    le = LabelEncoder()
    lables = le.fit_transform(lables)

    dataset_size = data.shape[0]
    data = data.reshape(dataset_size,-1)

    (trainX, testX, trainY, testY ) = train_test_split(data, lables, test_size= 0.25, random_state=42)

    model = KNeighborsClassifier(n_neighbors=3, n_jobs=-1)
    model.fit(trainX, trainY)

    imgtest = cv2.imread(imgpath)
    imgtest = cv2.resize(img, (32, 32), interpolation = cv2.INTER_AREA).reshape(1, -1)
    
    return label[model.predict(imgtest)[0]]
