import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time


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


def identifyAlly(pokemonNameDict, trainingDict, imgGray):
    ''' Test images are 384 x 256 '''
    ''' 23, 72 is top left '''
    ''' 102, 151 is bottom right '''
    tuples = []

    portion = imgGray[72:151 + 1, 23:102 + 1]
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

    print("The most likely ally is " + name + " with accuracy of " + str(round(value * 100, 2)) + "%")

    return number


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

    return number


def isShinyEnemy(enemyNumber):
    decimal = enemyNumber - int(enemyNumber)
    if 0.49 < decimal < 0.511:
        return True
    return False


def identifyAllPokemon(pokemonNameDict, imgRGB, imgGray, trainingDictAlly, allyNumber, trainingDictEnemy, enemyNumber):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (0, 0, 127)
    thickness = 1

    ''' Ally '''
    ''' 23, 72 is top left '''
    ''' 102, 151 is bottom right '''
    templateAlly = trainingDictAlly[allyNumber]

    w, h = templateAlly.shape[::-1]

    # crop = img[topIndex:bottomIndex + 1, leftIndex:rightIndex + 1]
    portionAlly = imgGray[72:151 + 1, 23:102 + 1]
    portionAllyCopy = getImgWithTemplateColors(templateAlly, portionAlly)

    res = cv2.matchTemplate(portionAllyCopy, templateAlly, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    left = top_left[0] + 23
    top = top_left[1] + 72
    top_left = left, top
    bottom_right = (left + w, top + h)

    cv2.rectangle(imgRGB, top_left, bottom_right, (255, 0, 0), 1)
    name = pokemonNameDict[math.floor(allyNumber)]
    imgRGB = cv2.putText(imgRGB, name, top_left, font, fontScale, color, thickness, cv2.LINE_AA)

    ''' Enemy '''
    ''' 152, 15 is top left '''
    ''' 231, 94 is bottom right '''
    templateEnemy = trainingDictEnemy[enemyNumber]

    w, h = templateEnemy.shape[::-1]

    # crop = img[topIndex:bottomIndex + 1, leftIndex:rightIndex + 1]
    portionEnemy = imgGray[15:94 + 1, 152:231 + 1]
    portionEnemyCopy = getImgWithTemplateColors(templateEnemy, portionEnemy)

    res = cv2.matchTemplate(portionEnemyCopy, templateEnemy, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    left = top_left[0] + 152
    top = top_left[1] + 15
    top_left = left, top
    bottom_right = (left + w, top + h)

    cv2.rectangle(imgRGB, top_left, bottom_right, (255, 0, 0), 1)
    name = pokemonNameDict[math.floor(enemyNumber)]
    imgRGB = cv2.putText(imgRGB, name, top_left, font, fontScale, color, thickness, cv2.LINE_AA)

    # Draw Rectangles around Search Areas
    # top_left = 23, 72
    # bottom_right = 102, 151
    # cv2.rectangle(imgRGB, top_left, bottom_right, (0, 255, 0), 1)
    # top_left = 152, 15
    # bottom_right = 231, 94
    # cv2.rectangle(imgRGB, top_left, bottom_right, (0, 255, 0), 1)

    cv2.imshow("", imgRGB)
