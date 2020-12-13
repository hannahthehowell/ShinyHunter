import uploadImages
import imageProcessing

import cv2
import time
import winsound
import pyautogui
import os


# Used to determine if the game is in a battle
def checkInBattle():
    try:
        # If it can find the health bar image, then the player is in a battle
        locationHealth = pyautogui.locateOnScreen("Images/HealthBar.png")
        if locationHealth is not None:
            print()
            return True
    except pyautogui.ImageNotFoundException:
        print("Health Bar was NOT found on the screen")
    except TypeError:
        print("TypeError")
        exit(2)

    return False


# Used to run the emulator using PyAutoGUI
def run(pokemonNameDict, enemyDict, upDown):
    # Remove testing screenshot if it already exists
    if os.path.exists("Screenshot.png"):
        os.remove("Screenshot.png")

    # Identify Desmume on screen via the options button
    try:
        left, top, width, height = pyautogui.locateOnScreen("Images/Options.png")
    except (pyautogui.ImageNotFoundException, TypeError):
        exit(1)

    # Move mouse to Desmume location and click
    pyautogui.click(x=left, y=(top + height + 5))

    # Counts the amount of Pokemon encountered
    encounters = 0

    # Master while loop - only exits if it finds a shiny Pokemon
    searching = True
    while searching:

        # Remove screenshot if it already exists
        if os.path.exists("Screenshot.png"):
            os.remove("Screenshot.png")

        # While loop that makes the character run
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
                time.sleep(0.8)
                pyautogui.keyUp('s')
            # run right
            else:
                pyautogui.keyDown('d')
                time.sleep(0.8)
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
        enemyNumber, percentSure = imageProcessing.identifyEnemy(pokemonNameDict, enemyDict, imgGray)

        # If less than 50% sure, try again - up to 3 tries before exiting
        if percentSure < 0.5:
            print("Not certain enough. Trying again.")
            # remove screenshot if it already exists
            if os.path.exists("Screenshot.png"):
                os.remove("Screenshot.png")

            # take screenshot - F12
            pyautogui.keyDown('f12')
            pyautogui.keyUp('f12')

            # rename to "Screenshot"
            pyautogui.write("Screenshot")
            pyautogui.press('enter')
            time.sleep(2)

            # image processing
            imgGray = cv2.imread("Screenshot.png", 0)
            enemyNumber, percentSure = imageProcessing.identifyEnemy(pokemonNameDict, enemyDict, imgGray)

            if percentSure < 0.5:
                print("Not certain enough. Trying one last time.\n")
                # remove screenshot if it already exists
                if os.path.exists("Screenshot.png"):
                    os.remove("Screenshot.png")

                # This time, wait until if can find the "Run" option on the screen
                while True:
                    try:
                        left, top, width, height = pyautogui.locateOnScreen("Images/Run.png")
                        break
                    except (pyautogui.ImageNotFoundException, TypeError):
                        print("...", end="")

                # take screenshot - F12
                pyautogui.keyDown('f12')
                pyautogui.keyUp('f12')

                # rename to "Screenshot"
                pyautogui.write("Screenshot")
                pyautogui.press('enter')
                time.sleep(2)

                # image processing
                imgGray = cv2.imread("Screenshot.png", 0)
                enemyNumber, percentSure = imageProcessing.identifyEnemy(pokemonNameDict, enemyDict, imgGray)

                if percentSure < 0.5:
                    # Exits if it can't accurately identify the Pokemon 3 times
                    print("Unknown Enemy Pokemon")
                    exit(3)

        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find enemy")

        # If the enemy Pokemon is shiny,
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

            print("IT'S SHINY")
            exit(5)  # toggle comment on this line to exit or beep
            while True:
                winsound.Beep(2000, 100)
                time.sleep(0.75)
        else:
            # identify Run on screen
            while True:
                try:
                    left, top, width, height = pyautogui.locateOnScreen("Images/Run.png")
                    break
                except (pyautogui.ImageNotFoundException, TypeError):
                    print("...", end="")
                    pass

            # Move mouse to Run location and click twice
            pyautogui.moveTo(x=(left + width / 2), y=(top + height / 2))
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.mouseUp()
            time.sleep(1)
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.mouseUp()
            time.sleep(1)


def main():
    # Populate a dictionary linking Pokemon name to number
    pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")

    # Ask the user which area type they will be hunting in
    # These correspond to the lists of wild Pokemon by area
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

    # Populate the list string based on the user's selection
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
    # Create a list of specific areas within the area type selected above
    areaList = uploadImages.loadList(listString)

    # User selects which area to hunt in
    print("Please select which area you'd like to hunt in")
    for i in range(len(areaList)):
        print(str(i+1) + ": " + areaList[i][0])

    selection = eval(input("\nSelection: "))
    while selection < 1 or selection > len(areaList):
        print("\nThat selection was invalid\n")
        selection = eval(input("Selection: "))

    # Get the specific area from the area type list
    selectionIndex = selection - 1
    huntingList = areaList[selectionIndex][1:]

    # Get a list of numbers corresponding to the names of Pokemon in the area
    huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, huntingList)

    # Get the folder name that's created, filled with reference images of Pokemon
    searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

    # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
    enemyDict = uploadImages.getImageDict(searchFolderName)

    # Ask the user if they'd like to run up and down or left and right
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

    # Final check to make sure the emulator is ready to be ran
    print("\nPlease make sure DeSmuMe is pulled up and your player is in " + areaList[selectionIndex][0])
    input("Press 'Enter' to continue ")

    # Run the emulator
    run(pokemonNameDict, enemyDict, upDown)


main()


# Used to test the wild Pokemon lists - primarily looks for typos
def testAllWildLists():
    pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
    listStrings = ["WildPokemonLists/HGSSWildPokemonListGrass.txt", "WildPokemonLists/HGSSWildPokemonListCave.txt", "WildPokemonLists/HGSSWildPokemonListBuilding.txt", "WildPokemonLists/HGSSWildPokemonListSurf.txt"]
    for listString in listStrings:
        areaList = uploadImages.loadList(listString)
        for area in areaList:
            print(area[0])
            huntingList = area[1:]
            huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, huntingList)
            print(huntingNumbers)


# testAllWildLists()
