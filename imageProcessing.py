import cv2
import numpy as np
import math


def pixelInRange(pixel, testSet):
    for color in testSet:
        if abs(int(pixel) - int(color)) < 2:
            return True
    return False


def getImgWithTemplateColors(template, portion):
    width, height = template.shape[::-1]
    templateSet = set()
    for i in range(height):
        for j in range(width):
            templateSet.add(template[i][j])

    portionCopy = np.copy(portion)
    width, height = portionCopy.shape[::-1]
    for i in range(height):
        for j in range(width):
            testing = portion[i][j]
            if not pixelInRange(testing, templateSet):
                portionCopy[i][j] = 254

    return portionCopy


def identifyEnemy(pokemonNameDict, trainingDict, imgGray):
    ''' Test images are 384 x 256 '''
    ''' 152, 15 is top left '''
    ''' 231, 94 is bottom right '''
    tuples = []

    portion = imgGray[15:94 + 1, 152:231 + 1]
    for key in trainingDict:
        template = trainingDict[key]
        portionCopy = getImgWithTemplateColors(template, portion)

        res = cv2.matchTemplate(portionCopy, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        tuples.append([key, max_val])

    tuples.sort(key=lambda x: x[1])
    tuples.reverse()

    number = tuples[0][0]
    value = tuples[0][1]

    name = pokemonNameDict[math.floor(number)]

    print("The most likely enemy is " + name + " with accuracy of " + str(round(value * 100, 2)) + "%")

    return number, value


def isShinyEnemy(enemyNumber):
    decimal = enemyNumber - int(enemyNumber)
    if 0.49 < decimal < 0.511:
        return True
    return False
