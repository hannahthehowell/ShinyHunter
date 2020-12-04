import uploadImages
import imageProcessing

import cv2
import time
import winsound
import pyautogui
import os


def checkInBattle():
    try:
        locationRun = pyautogui.locateOnScreen("Images/Run.png")
        locationOption = pyautogui.locateOnScreen("Images/Options.png")
        if locationRun is None and locationOption is None:
            for i in range(7):
                print(".", end="")
                time.sleep(0.5)
        elif locationRun is None:
            pass
        else:
            print()
            return True
    except pyautogui.ImageNotFoundException:
        print("RUN was NOT found on the screen")
    except TypeError:
        print("TypeError")
        exit(2)

    return False


def run(pokemonNameDict, enemyDict, upDown):
    # remove screenshot if it already exists
    if os.path.exists("Screenshot.png"):
        os.remove("Screenshot.png")

    # identify Desmume on screen
    try:
        left, top, width, height = pyautogui.locateOnScreen("Images/Options.png")
    except (pyautogui.ImageNotFoundException, TypeError):
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
        imgGray = cv2.imread("Screenshot.png", 0)

        startTime = time.time()
        enemyNumber = imageProcessing.identifyEnemy(pokemonNameDict, enemyDict, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find enemy")

        if imageProcessing.isShinyEnemy(enemyNumber):
            searching = False
            try:
                left, top, width, height = pyautogui.locateOnScreen("Images/Pause.png")
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
                left, top, width, height = pyautogui.locateOnScreen("Images/Run.png")
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

    listString = "WildPokemonLists/"
    listString += "HGSSWildPokemonList"
    if selection == 1:
        listString += "Grass"
    elif selection == 2:
        listString += "Cave"
    elif selection == 3:
        listString += "Building"
    elif selection == 4:
        listString += "Surf"
    else:
        exit(2)

    listString += ".txt"
    areaList = uploadImages.loadList(listString)

    print("Please select which area you'd like to hunt in")
    for i in range(len(areaList)):
        print(str(i+1) + ": " + areaList[i][0])

    selection = eval(input("\nSelection: "))
    while selection < 1 or selection > len(areaList):
        print("\nThat selection was invalid\n")
        selection = eval(input("Selection: "))

    selectionIndex = selection - 1
    huntingList = areaList[selectionIndex][1:]

    huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, huntingList)

    searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

    enemyDict = uploadImages.getImageDict(searchFolderName)

    print("\nWould you like to run")
    print("1: Up and Down")
    print("2: Left and Right")
    selection = eval(input("Selection: "))
    while selection != 1 and selection != 2:
        print("\nWould you like to run")
        print("1: Up and Down")
        print("2: Left and Right")
        selection = eval(input("Selection: "))

    upDown = True
    if selection == 2:
        upDown = False
    else:
        exit(5)
    print("\nPlease make sure DeSmuMe is pulled up and your player is in " + areaList[selectionIndex][0])
    input("Press 'Enter' to continue ")
    run(pokemonNameDict, enemyDict, upDown)


main()


def testAllWildLists():
    pokemonNameDict = uploadImages.loadDict()
    listStrings = ["WildPokemonLists/HGSSWildPokemonListGrass.txt", "WildPokemonLists/HGSSWildPokemonListCave.txt", "WildPokemonLists/HGSSWildPokemonListBuilding.txt", "WildPokemonLists/HGSSWildPokemonListSurf.txt"]
    for listString in listStrings:
        areaList = uploadImages.loadList(listString)
        for area in areaList:
            print(area[0])
            huntingList = area[1:]
            huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, huntingList)
            print(huntingNumbers)


# testAllWildLists()
