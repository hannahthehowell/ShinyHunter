import cv2
import numpy as np
from PIL import Image


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


# Used to get the match percentage using matchTemplate from cv2
def getMaxVal(template, portion):
    portionCopy = getImgWithTemplateColors(template, portion)

    res = cv2.matchTemplate(portionCopy, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    return max_val


# Used to identify the enemy sprite in a battle
def identifyEnemy(trainingDict, imgGray):
    ''' Screenshots are 384 x 256 '''
    ''' 152, 15 is top left '''
    ''' 231, 94 is bottom right '''

    # Create a list of lists that contain the Pokemon's number with its corresponding accuracy value
    valuePairs = []

    # Identify the portion of the test image that corresponds to the Pokemon
    portion = imgGray[15:94 + 1, 152:231 + 1]

    # For every possible Pokemon, calculate its accuracy
    for key in trainingDict:
        template = trainingDict[key]
        max_val = getMaxVal(template, portion)

        # Append the Pokemon's number with its corresponding accuracy value
        valuePairs.append([key, max_val])

    # Reverse sort the list so the Pokemon with the highest accuracy is on top
    valuePairs.sort(key=lambda x: x[1])
    valuePairs.reverse()

    # Pokemon with highest accuracy is at index 0
    fileNameOfClosestMatch = valuePairs[0][0]
    percentSure = valuePairs[0][1]

    return fileNameOfClosestMatch, percentSure


# Used to determine if the Pokemon is shiny based on the naming scheme
def isShinyPokemon(fileNameOfClosestMatch):
    return fileNameOfClosestMatch.endswith("S")


# Used to identify which sprite best matches the hatched Pokemon
def identifyHatched(trainingDict, imgGray):
    ''' Screenshots are 384 x 256 '''
    ''' 88, 56 is top left '''
    ''' 167, 135 is bottom right '''

    # Create a list of lists that contain the Pokemon's number with its corresponding accuracy value
    valuePairs = []

    # Identify the portion of the test image that corresponds to the Pokemon
    portion = imgGray[56:135 + 1, 88:167 + 1]

    # For every possible Pokemon, calculate its accuracy
    for key in trainingDict:
        template = trainingDict[key]
        max_val = getMaxVal(template, portion)

        # Append the Pokemon's number with its corresponding accuracy value
        valuePairs.append([key, max_val])

    # Reverse sort the list so the Pokemon with the highest accuracy is on top
    valuePairs.sort(key=lambda x: x[1])
    valuePairs.reverse()

    # Pokemon with highest accuracy is at index 0
    fileNameOfClosestMatch = valuePairs[0][0]

    return fileNameOfClosestMatch


# Used to remove the greenish color from behind the hatched Pokemon
def removeEggBackground(imgColor):
    # List of green/mint colors in the screenshot
    mint = np.array([[248, 248, 248],
                     [240, 248, 240],
                     [248, 248, 232],

                     [240, 248, 216],
                     [224, 240, 200],
                     [224, 232, 184],

                     [216, 224, 168],
                     [160, 192, 64],
                     [152, 184, 64],

                     [216, 224, 160],
                     [200, 224, 144],
                     [192, 216, 128],

                     [184, 208, 104],
                     [168, 200, 88],
                     [160, 192, 72]])

    whiteCell = np.array([254, 254, 254])

    # For each cell in desired portion, remove background and save to new variable
    imgColorScraped = imgColor.copy()
    for row in range(56, 136):
        for col in range(88, 168):
            for m in range(mint.shape[0]):
                mintColor = mint[m]
                imagePixel = imgColorScraped[row][col]
                if np.array_equal(mintColor, imagePixel):
                    imgColorScraped[row][col] = whiteCell
                    break

    # Convert from BGR to RGB
    imgColorScraped = imgColorScraped[..., ::-1].copy()

    # Turn np array into image
    data = Image.fromarray(imgColorScraped)

    # Saving the final output
    data.save("Screenshot.png")


# Used to determine if the daycare man is facing left
def manFacingLeft(imgGray, daycareDoor=False):
    ''' Screenshots are 384 x 256 '''
    ''' 198, 63 is top left '''
    ''' 218, 87 is bottom right '''

    # Create a dictionary that contain the each direction with its corresponding accuracy value
    valuePairs = {
        "Down": 0,
        "Left": 0
    }

    # Identify the portion of the screenshot that corresponds to the man
    if not daycareDoor:
        portion = imgGray[63:87 + 1, 198:218 + 1]
    else:
        portion = imgGray[64:86 + 1, 70:89 + 1]

    # For each direction, calculate its accuracy
    # Down
    template_down = cv2.imread("AnchorImages/DownMan-D.PNG", 0)
    valuePairs["Down"] = getMaxVal(template_down, portion)

    # Left
    template_left = cv2.imread("AnchorImages/LeftMan-D.PNG", 0)
    valuePairs["Left"] = getMaxVal(template_left, portion)

    # Return if it is more likely that he's facing left
    return valuePairs["Down"] < valuePairs["Left"]


# Used to determine if the player is at the lakeside
def isAtLakeside(imgGray):
    ''' Screenshots are 384 x 256 '''
    ''' 218, 64 is top left '''
    ''' 233, 79 is bottom right '''

    # Identify the portion of the screenshot that should correspond to the sign
    portion = imgGray[64:79 + 1, 218:233 + 1]
    template_sign = cv2.imread("AnchorImages/sign.png", 0)

    # Make the set of numbers that correspond to the sign
    template_set = set()
    for row in range(len(template_sign)):
        for col in range(row):
            template_set.add(template_sign[row][col])

    # Make the set of numbers that correspond to the supposed sign's location
    portion_set = set()
    for row in range(len(portion)):
        for col in range(row):
            portion_set.add(portion[row][col])

    # If the sets have a different number of items, return false
    if len(template_set) != len(portion_set):
        return False

    # Turn the set into a list and sort it
    portion_list = list(portion_set)
    portion_list.sort()

    # Test a sample set of pixels to the numbers in the set to make sure it follows the sign's pattern
    if portion[8][5] != portion_list[0] or portion[12][11] != portion_list[0]:
        return False
    if portion[3][7] != portion_list[1] or portion[14][1] != portion_list[1]:
        return False
    if portion[6][4] != portion_list[2] or portion[10][12] != portion_list[2]:
        return False
    if portion[0][0] != portion_list[3] or portion[1][15] != portion_list[3]:
        return False

    return True
