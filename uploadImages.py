import cv2
import numpy as np
import os
import csv
import shutil


def loadDict():
    inputFile = csv.reader(open("PokemonListByNumber.csv", "r"))
    dictionary = {}
    for row in inputFile:
        number, name = row
        dictionary[int(number)] = name
    return dictionary


def loadList(inputString):
    lineList = [line.rstrip('\n') for line in open(inputString)]
    masterList = []
    for i in range(len(lineList)):
        masterList.append(lineList[i].split(", "))
    return masterList


def listToNumbers(pokemonNameDict, huntingList):
    numberList = []
    for i in range(len(huntingList)):
        pokemonName = huntingList[i]
        for number, name in pokemonNameDict.items():
            if pokemonName == name:
                numberList.append(int(number))
                break
        assert len(numberList) == (i+1), ("Pokemon Name Misspelled:", pokemonName)

    return numberList


def createAndFillSearchFolder(huntingNumbers):
    """ This For-loop found at https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder """
    folder = "SearchImages"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for filename in os.listdir("EnemySprites"):
        path = "EnemySprites/" + filename
        if float(filename.strip(".png"))//1 in huntingNumbers:
            shutil.copy(path, "SearchImages/")

    return "SearchImages"


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


def getImageDict(folderString):
    imageDict = {}
    for filename in os.listdir(folderString):
        path = folderString + "/" + filename
        im = cv2.imread(path, 0)
        imc = cropImgGray(im, float(filename.strip(".png")))
        imageDict[float(filename.strip(".png"))] = imc
    return imageDict
