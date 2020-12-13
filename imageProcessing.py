import cv2
import numpy as np
import math


# Used to determine if a pixel is within 2 points of any number in a test set of colors
def pixelInRange(pixel, testSet):
    for color in testSet:
        if abs(int(pixel) - int(color)) < 2:
            return True
    return False


# Used to modify the test image so identifying Pokemon is easier
def getImgWithTemplateColors(template, portion):
    width, height = template.shape[::-1]

    # Add every unique pixel color in the template image to a set
    templateSet = set()
    for i in range(height):
        for j in range(width):
            templateSet.add(template[i][j])

    # Make a copy of the portion
    portionCopy = np.copy(portion)
    width, height = portionCopy.shape[::-1]
    # Loop through every pixel in the portion
    for i in range(height):
        for j in range(width):
            testing = portion[i][j]
            # If it is unlikely that the pixel is part of the template Pokemon, then set pixel to 254
            if not pixelInRange(testing, templateSet):
                portionCopy[i][j] = 254

    # Return the modified portion copy
    return portionCopy


def identifyEnemy(pokemonNameDict, trainingDict, imgGray):
    ''' Test images are 384 x 256 '''
    ''' 152, 15 is top left '''
    ''' 231, 94 is bottom right '''

    # Create a list of lists that contain the Pokemon's number with its corresponding accuracy value
    valuePairs = []

    # Identify the portion of the test image that corresponds to the Pokemon
    portion = imgGray[15:94 + 1, 152:231 + 1]

    # For every possible Pokemon, calculate its accuracy
    for key in trainingDict:
        template = trainingDict[key]
        portionCopy = getImgWithTemplateColors(template, portion)

        res = cv2.matchTemplate(portionCopy, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # append the Pokemon's number with its corresponding accuracy value
        valuePairs.append([key, max_val])

    # Reverse sort the list so the Pokemon with the highest accuracy is on top
    valuePairs.sort(key=lambda x: x[1])
    valuePairs.reverse()

    # Pokemon with highest accuracy is at index 0
    number = valuePairs[0][0]
    value = valuePairs[0][1]

    name = pokemonNameDict[math.floor(number)]

    print("The most likely enemy is " + name + " with accuracy of " + str(round(value * 100, 2)) + "%")

    return number, value


# Used to determine if the enemy Pokemon is shiny based on the naming scheme
def isShinyEnemy(enemyNumber):
    decimal = enemyNumber - int(enemyNumber)
    if 0.49 < decimal < 0.511:
        return True
    return False
