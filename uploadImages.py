import cv2
import numpy as np
import os
import csv


def getTrainingDict(folderString):
    imageDict = {}
    for filename in os.listdir(folderString):
        path = folderString + "/" + filename
        im = cv2.imread(path, 0)
        imc = cropImgGray(im, float(filename.strip(".png")))
        imageDict[float(filename.strip(".png"))] = imc
    return imageDict


def getTestingList(folderString):
    imageSet = []
    for filename in os.listdir(folderString):
        im = cv2.imread(os.path.join(folderString, filename))
        imageSet.append(im)
    return imageSet


def makeListGray(image_set):
    bwSet = []
    for image in image_set:
        bwSet.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    return bwSet


def loadDict():
    input_file = csv.reader(open("PokemonListByNumber.csv", "r"))
    dictionary = {}
    for row in input_file:
        number, name = row
        dictionary[int(number)] = name
    return dictionary


def cropImgGray(img, key):
    width, height = img.shape[::-1]

    topIndex = height - 1
    bottomIndex = 0
    leftIndex = width - 1
    rightIndex = 0

    white = 255
    black = 0

    targetColor = img[0][0]
    if targetColor != white and targetColor != black:
        targetColor = white
        print("We may have a problem in cropping this image")
        print(key)

    for row in range(height):
        for col in range(width):
            if img[row][col] != targetColor:
                if row < topIndex:
                    topIndex = row
                if row > bottomIndex:
                    bottomIndex = row
                if col < leftIndex:
                    leftIndex = col
                if col > rightIndex:
                    rightIndex = col

    crop = img[topIndex:bottomIndex+1, leftIndex:rightIndex+1]

    width, height = crop.shape[::-1]

    cropCopy = np.copy(crop)
    for row in range(height):
        for col in range(width):
            if crop[row][col] == targetColor:
                cropCopy[row][col] = 254
            else:
                cropCopy[row][col] = crop[row][col] * 0.9784948631

    return cropCopy
