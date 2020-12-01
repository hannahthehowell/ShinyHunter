import cv2
import numpy as np
import os
import csv
from matplotlib import pyplot as plt
import math
import random
import time


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


# def crop_img(img):
#     color, width, height = img.shape[::-1]
#
#     topIndex = height - 1
#     bottomIndex = 0
#     leftIndex = width - 1
#     rightIndex = 0
#
#     white = [255, 255, 255]
#
#     for row in range(height):
#         for col in range(width):
#             if all(img[row][col] != white):
#                 if row < topIndex:
#                     topIndex = row
#                 if row > bottomIndex:
#                     bottomIndex = row
#                 if col < leftIndex:
#                     leftIndex = col
#                 if col > rightIndex:
#                     rightIndex = col
#
#     crop = img[topIndex:bottomIndex+1, leftIndex:rightIndex+1]
#
#     # plt.subplot(121),
#     # plt.imshow(img)
#     # plt.title('Original Image'),
#     # plt.xticks([]), plt.yticks([])
#     # plt.subplot(122),
#     # plt.imshow(crop)
#     # plt.title('Cropped Image'),
#     # plt.xticks([]), plt.yticks([])
#     # plt.show()
#
#     return crop


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


# def identifyAllPokemon(pokemonNameDict, trainingDict, imgRGB, imgGray):
#     font = cv2.FONT_HERSHEY_PLAIN
#     fontScale = 1
#     color = (255, 255, 255)
#     thickness = 1
#
#     for key in trainingDict:
#         template = trainingDict[key]
#
#         w, h = template.shape[::-1]
#
#         # crop = img[topIndex:bottomIndex + 1, leftIndex:rightIndex + 1]
#         portion = imgGray[0:192+1, 0:256+1]
#
#         res = cv2.matchTemplate(portion, template, cv2.TM_CCOEFF_NORMED)
#
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#
#         ''' When Black - 0.78 is where Chikorita false positive disappears; Weedle isn't found after 0.75 '''
#         ''' When white - 0.95 gets most light pokemon'''
#         if max_val > 0.96:  # TODO
#             top_left = max_loc
#             bottom_right = (top_left[0] + w, top_left[1] + h)
#
#             cv2.rectangle(imgRGB, top_left, bottom_right, (255, 0, 0), 1)
#             name = pokemonNameDict[math.floor(key)]
#             imgRGB = cv2.putText(imgRGB, name, top_left, font, fontScale, color, thickness, cv2.LINE_AA)
#
#     cv2.imshow("", imgRGB)


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

        # templateSetExpand = set()
        # for item in templateSet:
        #     templateSetExpand.add(item)
        #     templateSetExpand.add(item + 1)
        #     templateSetExpand.add(item - 1)
        #     templateSetExpand.add(item + 2)
        #     templateSetExpand.add(item - 2)
        # portionCopy[not portionCopy in templateSetExpand] = 254

        # plt.subplot(131),
        # plt.imshow(portion, cmap='gray')
        # plt.title('Portion Image'),
        # plt.xticks([]), plt.yticks([])
        #
        # plt.subplot(132),
        # plt.imshow(portionCopy, cmap='gray')
        # plt.title('Modified Portion'),
        # plt.xticks([]), plt.yticks([])
        #
        # plt.subplot(133),
        # plt.imshow(template, cmap='gray')
        # plt.title('Template Image'),
        # plt.xticks([]), plt.yticks([])
        #
        # plt.show()

        res = cv2.matchTemplate(portionCopy, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # number = math.floor(key)
        tuples.append([key, max_val])

    tuples.sort(key=lambda x: x[1])
    tuples.reverse()

    number = tuples[0][0]
    value = tuples[0][1]

    name = pokemonNameDict[math.floor(number)]

    print("The most likely enemy is " + name + " with accuracy of " + str(round(value * 100, 2)) + "%")

    # for i in range(8):
    #     print(tuples[i])

    return number


def identifyAlly(pokemonNameDict, trainingDict, imgGray):
    ''' Test images are 384 x 256 '''
    ''' 23, 72 is top left '''
    ''' 102, 151 is bottom right '''
    tuples = []

    portion = imgGray[72:151 + 1, 23:102 + 1]
    for key in trainingDict:
        template = trainingDict[key]

        portionCopy = getImgWithTemplateColors(template, portion)

        # templateSetExpand = set()
        # for item in templateSet:
        #     templateSetExpand.add(item)
        #     templateSetExpand.add(item + 1)
        #     templateSetExpand.add(item - 1)
        #     templateSetExpand.add(item + 2)
        #     templateSetExpand.add(item - 2)
        # portionCopy[not portionCopy in templateSetExpand] = 254

        # plt.subplot(131),
        # plt.imshow(portion, cmap='gray')
        # plt.title('Portion Image'),
        # plt.xticks([]), plt.yticks([])
        #
        # plt.subplot(132),
        # plt.imshow(portionCopy, cmap='gray')
        # plt.title('Modified Portion'),
        # plt.xticks([]), plt.yticks([])
        #
        # plt.subplot(133),
        # plt.imshow(template, cmap='gray')
        # plt.title('Template Image'),
        # plt.xticks([]), plt.yticks([])
        #
        # plt.show()

        res = cv2.matchTemplate(portionCopy, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # number = math.floor(key)
        tuples.append([key, max_val])

    tuples.sort(key=lambda x: x[1])
    tuples.reverse()

    number = tuples[0][0]
    value = tuples[0][1]

    name = pokemonNameDict[math.floor(number)]

    print("The most likely ally is " + name + " with accuracy of " + str(round(value * 100, 2)) + "%")

    # for i in range(8):
    #     print(tuples[i])

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


def main():
    pokemonNameDict = loadDict()

    folderStringAlly = "training_sprites_ally"
    trainingDictAlly = getTrainingDict(folderStringAlly)

    folderStringEnemy = "training_sprites_enemy"
    trainingDictEnemy = getTrainingDict(folderStringEnemy)

    folderStringTest = "testing_images_grass"
    # folderStringTest = "testing_images_cave"

    # folderStringTest = "testing_images_path"
    # folderStringTest = "testing_images_buildings"
    # folderStringTest = "advanced_testing"

    # folderStringTest = "testing_images_shiny"

    testingSetRGB = getTestingList(folderStringTest)
    testingListGray = makeListGray(testingSetRGB)

    for i in range(len(testingSetRGB)):
        imgRGB = testingSetRGB[i]
        imgGray = testingListGray[i]

        startTime = time.time()
        allyNumber = identifyAlly(pokemonNameDict, trainingDictAlly, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find ally")

        startTime = time.time()
        enemyNumber = identifyEnemy(pokemonNameDict, trainingDictEnemy, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find enemy")

        identifyAllPokemon(pokemonNameDict, imgRGB, imgGray, trainingDictAlly, allyNumber, trainingDictEnemy, enemyNumber)

        if isShinyEnemy(enemyNumber):
            print("IT'S SHINY")
            # while True:
            #     print("IT'S SHINY")
            #     time.sleep(1)

        cv2.waitKey()
        print()

    # plt.subplot(221),
    # plt.imshow(img, cmap='gray')
    # plt.title('Original Image'),
    # plt.xticks([]), plt.yticks([])
    #
    # plt.subplot(222),
    # plt.imshow(edges, cmap='gray')
    # plt.title('Edge Image'),
    # plt.xticks([]), plt.yticks([])
    #
    # img2 = trainingDictEnemy[19]
    # edges2 = cv2.Canny(img2, 100, 200)
    #
    # plt.subplot(223),
    # plt.imshow(img2, cmap='gray')
    # plt.title('Original Image'),
    # plt.xticks([]), plt.yticks([])
    #
    # plt.subplot(224),
    # plt.imshow(edges2, cmap='gray')
    # plt.title('Edge Image'),
    # plt.xticks([]), plt.yticks([])
    #
    # plt.show()


main()
