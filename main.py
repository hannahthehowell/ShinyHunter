import uploadImages
import imageProcessing

import cv2
import time
import winsound
import pyautogui
import os
import random


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


def run(pokemonNameDict, trainingDictAlly, trainingDictEnemy, upDown):
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
            if upDown:
                pyautogui.keyDown('w')
                time.sleep(0.6)
                pyautogui.keyUp('w')
            # run left
            else:
                pyautogui.keyDown('a')
                time.sleep(0.6)
                pyautogui.keyUp('a')

            # check if in battle
            if checkInBattle():
                break

            # run down
            if upDown:
                pyautogui.keyDown('s')
                time.sleep(0.6)
                pyautogui.keyUp('s')
            # run right
            else:
                pyautogui.keyDown('d')
                time.sleep(0.6)
                pyautogui.keyUp('d')

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
            searching = False
            try:
                left, top, width, height = pyautogui.locateOnScreen("Pause.png")
            except (pyautogui.ImageNotFoundException, TypeError):
                print("Pause was NOT found on the screen")
                exit(4)

            # Move mouse to Pause location and click
            pyautogui.moveTo(x=(left + width / 2), y=(top + height / 2))
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.mouseUp()

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
            pyautogui.moveTo(x=(left + width / 2), y=(top + height / 2))
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.mouseUp()


def main():
    pokemonNameDict = uploadImages.loadDict()

    print("What area will you be shiny hunting in?")
    print("1: Walking in Grass")
    print("2: Walking in a Cave")
    print("3: Walking in a Building")
    print("4: Surfing (anywhere)")

    selection = eval(input("Selection: "))

    while selection != 1 and selection != 2 and selection != 3 and selection != 4:
        print("\nThat selection was invalid\n")
        print("What area will you be shiny hunting in?")
        print("1: Walking in Grass")
        print("2: Walking in a Cave")
        print("3: Walking in a Building")
        print("4: Surfing (anywhere)")
        selection = eval(input("Selection: "))

    if selection == 1:
        pass
    elif selection == 2:
        pass
    elif selection == 3:
        pass
    else:
        exit(2)


    folderStringAlly = "training_sprites_ally"
    trainingDictAlly = uploadImages.getTrainingDict(folderStringAlly)

    folderStringEnemy = "training_sprites_enemy"
    trainingDictEnemy = uploadImages.getTrainingDict(folderStringEnemy)

    print("Pick which mode you'd like to run")
    print("1: Testing Mode")
    print("2: Running Mode")
    selection = eval(input("Selection: "))



    if selection == 1:
        testing(pokemonNameDict, trainingDictAlly, trainingDictEnemy)
    elif selection == 2:
        print("\nWould you like to run")
        print("1: Up and Down")
        print("2: Left and Right")
        selection = eval(input("Selection: "))
        while selection != 1 and selection != 2:
            print("\nWould you like to run")
            print("1: Up and Down")
            print("2: Left and Right")
            selection = eval(input("Selection: "))
        if selection == 1:
            upDown = True
        elif selection == 2:
            upDown = False
        else:
            exit(5)
        print("\nPlease make sure DeSmuMe is pulled up and your player is in the grass or a cave")
        input("Press 'Enter' to continue ")
        run(pokemonNameDict, trainingDictAlly, trainingDictEnemy, upDown)


main()
