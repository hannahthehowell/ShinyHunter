import uploadImages
import imageProcessing

import cv2
import time
import winsound
import pyautogui
import os
import glob


def checkInBattle():
    try:
        locationRun = pyautogui.locateOnScreen("Run.png")
        locationOption = pyautogui.locateOnScreen("Options.png")
        if locationRun is None and locationOption is None:
            for i in range(5):
                print(".", end="")
                time.sleep(0.5)
        elif locationRun is None:
            # print("RUN was NOT found on the screen")
            pass
        else:
            print()
            # print("RUN was found on the screen")
            return True
    except pyautogui.ImageNotFoundException:
        print("RUN was NOT found on the screen")
    except TypeError:
        print("TypeError")
        exit(2)

    return False


def main():
    pokemonNameDict = uploadImages.loadDict()

    folderStringAlly = "training_sprites_ally"
    trainingDictAlly = uploadImages.getTrainingDict(folderStringAlly)

    folderStringEnemy = "training_sprites_enemy"
    trainingDictEnemy = uploadImages.getTrainingDict(folderStringEnemy)

    # remove screenshot if it already exists
    if os.path.exists("Screenshot.png"):
        os.remove("Screenshot.png")
    else:
        # print("The file does not exist")
        pass

    # identify Desmume on screen
    try:
        left, top, width, height = pyautogui.locateOnScreen("Options.png")
        # print("DeSmuMe was found on the screen")
    except (pyautogui.ImageNotFoundException, TypeError):
        # print("DeSmuMe was NOT found on the screen")
        exit(1)

    # Move mouse to Desmume location and click
    pyautogui.click(x=left, y=(top + height + 5))

    # master while loop
    encounters = 0
    searching = True
    while searching:

        # remove screenshot if it already exists
        if os.path.exists("Screenshot.png"):
            os.remove("Screenshot.png")
        else:
            # print("The file does not exist")
            pass

        # running while loop
        inBattle = False
        while not inBattle:
            # check if in battle
            if checkInBattle():
                break

            # run up
            pyautogui.keyDown('w')
            time.sleep(0.6)
            pyautogui.keyUp('w')

            # check if in battle
            if checkInBattle():
                break

            # run down,
            pyautogui.keyDown('s')
            time.sleep(0.6)
            pyautogui.keyUp('s')

        encounters += 1
        print("Encounters:", encounters)

        # take screenshot - F12
        pyautogui.keyDown('f12')
        pyautogui.keyUp('f12')

        # rename to "Screenshot"
        pyautogui.write("Screenshot")
        pyautogui.press('enter')
        time.sleep(2)

        # image processing
        imgRGB = cv2.imread("Screenshot.png")
        imgGray = cv2.imread("Screenshot.png", 0)

        startTime = time.time()
        allyNumber = imageProcessing.identifyAlly(pokemonNameDict, trainingDictAlly, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find ally")

        startTime = time.time()
        enemyNumber = imageProcessing.identifyEnemy(pokemonNameDict, trainingDictEnemy, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find enemy")

        # imageProcessing.identifyAllPokemon(pokemonNameDict, imgRGB, imgGray, trainingDictAlly, allyNumber, trainingDictEnemy, enemyNumber)
        # time.sleep(2)

        if imageProcessing.isShinyEnemy(enemyNumber):
            # print("IT'S SHINY")
            searching = False
            while True:
                print("IT'S SHINY")
                winsound.Beep(2000, 100)
                time.sleep(0.75)
        else:
            # identify Run on screen
            try:
                left, top, width, height = pyautogui.locateOnScreen("Run.png")
                # print("RUN was found on the screen again")
            except (pyautogui.ImageNotFoundException, TypeError):
                print("RUN was NOT found on the screen")
                exit(3)

            # Move mouse to Run location and click
            pyautogui.moveTo(x=(left + width/2), y=(top + height/2))
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.mouseUp()

        # searching = False



# def main():
#     pokemonNameDict = uploadImages.loadDict()
#
#     folderStringAlly = "training_sprites_ally"
#     trainingDictAlly = uploadImages.getTrainingDict(folderStringAlly)
#
#     folderStringEnemy = "training_sprites_enemy"
#     trainingDictEnemy = uploadImages.getTrainingDict(folderStringEnemy)

    # folderStringTest = "testing_images_grass"
    # # folderStringTest = "testing_images_cave"
    #
    # # folderStringTest = "testing_images_path"
    # # folderStringTest = "testing_images_buildings"
    # # folderStringTest = "advanced_testing"
    #
    # # folderStringTest = "testing_images_shiny"
    #
    # testingSetRGB = uploadImages.getTestingList(folderStringTest)
    # testingListGray = uploadImages.makeListGray(testingSetRGB)
    #
    # for i in range(len(testingSetRGB)):
    #     imgRGB = testingSetRGB[i]
    #     imgGray = testingListGray[i]
    #
    #     startTime = time.time()
    #     allyNumber = imageProcessing.identifyAlly(pokemonNameDict, trainingDictAlly, imgGray)
    #     endTime = time.time()
    #     print(round(endTime - startTime, 5), "seconds to find ally")
    #
    #     startTime = time.time()
    #     enemyNumber = imageProcessing.identifyEnemy(pokemonNameDict, trainingDictEnemy, imgGray)
    #     endTime = time.time()
    #     print(round(endTime - startTime, 5), "seconds to find enemy")
    #
    #     imageProcessing.identifyAllPokemon(pokemonNameDict, imgRGB, imgGray, trainingDictAlly, allyNumber, trainingDictEnemy, enemyNumber)
    #
    #     if imageProcessing.isShinyEnemy(enemyNumber):
    #         print("IT'S SHINY")
    #         # while True:
    #         #     print("IT'S SHINY")
    #         #     winsound.Beep(2000, 100)
    #         #     time.sleep(2)
    #
    #     cv2.waitKey()
    #     print()

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
