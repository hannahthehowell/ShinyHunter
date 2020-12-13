import cv2
import numpy as np
import os
import csv
import shutil


# Used to create a dictionary of Pokemon names and numbers
def loadDict(fileName):
    inputFile = csv.reader(open(fileName, "r"))
    dictionary = {}
    for row in inputFile:
        number, name = row
        dictionary[int(number)] = name
    return dictionary


# Used to load a list of locations and their corresponding wild Pokemon available
def loadList(inputString):
    lineList = [line.rstrip('\n') for line in open(inputString)]
    masterList = []
    for i in range(len(lineList)):
        masterList.append(lineList[i].split(", "))
    return masterList


# Used to convert a list of Pokemon names to their corresponding numbers
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


# Used to create and fill a folder with appropriate search images
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


# Used to crop a training image such that there isn't excessive whitespace surrounding the image
def cropImgGray(img, key):
    width, height = img.shape[::-1]

    # initializes crop indices to max values
    topIndex = height - 1
    bottomIndex = 0
    leftIndex = width - 1
    rightIndex = 0

    white = 255
    black = 0

    # Checks to make sure the image can be properly cropped
    targetColor = img[0][0]
    if targetColor != white and targetColor != black:
        targetColor = white
        print("We may have a problem in cropping this image")
        print(key)

    # Determine what the max and min width and heights to crop the image to tightly
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

    # Crop the image
    crop = img[topIndex:bottomIndex+1, leftIndex:rightIndex+1]

    width, height = crop.shape[::-1]

    # Makes a copy of the crop and alters the image values slightly
    cropCopy = np.copy(crop)
    for row in range(height):
        for col in range(width):
            if crop[row][col] == targetColor:
                cropCopy[row][col] = 254
            else:
                cropCopy[row][col] = crop[row][col] * 0.9784948631  # constant aligns testing and training image colors

    # Return the cropped image with the constant adjustment
    return cropCopy


# Used to create a dictionary of training images
def getImageDict(folderString):
    imageDict = {}
    for filename in os.listdir(folderString):
        path = folderString + "/" + filename
        im = cv2.imread(path, 0)
        imc = cropImgGray(im, float(filename.strip(".png")))
        imageDict[float(filename.strip(".png"))] = imc
    return imageDict
