import uploadImages
import imageProcessing
import ShinyHuntLib as shl

import time
import pyautogui


totalEncountered = 0


# Used to determine if the game is in a battle
def checkInBattle():
    return shl.isImageFound("HealthBar")


# Used to run the emulator using PyAutoGUI
def run(pokemonNameDict, enemyDict, upDown):
    global totalEncountered

    # Remove testing screenshot if it already exists
    shl.removeScreenshot()

    shl.identifyDeSmuME()

    # Master while loop - only exits if it finds a shiny Pokemon
    searching = True
    while searching:
        # If it has been about an hour, reset ROM
        if totalEncountered % 180 == 0 and totalEncountered != 0:
            print("Resetting ROM")
            time.sleep(3)
            shl.resetROM()

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

        totalEncountered += 1
        print("Encounters:", totalEncountered)

        imgGray = shl.getScreenshot()
        startTime = time.time()
        fileNameOfClosestMatch, percentSure = imageProcessing.identifyEnemy(enemyDict, imgGray)
        name = pokemonNameDict[int(fileNameOfClosestMatch[0:3])]
        print("The most likely enemy is " + name + " with accuracy of " + str(round(percentSure * 100, 2)) + "%")

        # If less than 50% sure, try again - up to 3 tries before exiting
        if percentSure < 0.5:
            print("Not certain enough. Trying again.")

            imgGray = shl.getScreenshot()
            fileNameOfClosestMatch, percentSure = imageProcessing.identifyEnemy(enemyDict, imgGray)
            name = pokemonNameDict[int(fileNameOfClosestMatch[0:3])]
            print("The most likely enemy is " + name + " with accuracy of " + str(round(percentSure * 100, 2)) + "%")

            if percentSure < 0.5:
                print("Not certain enough. Trying one last time.\n")

                # This time, wait until if can find the "Run" option on the screen
                while True:
                    if shl.isImageFound("Run"):
                        break
                    else:
                        print("...", end="")

                imgGray = shl.getScreenshot()
                fileNameOfClosestMatch, percentSure = imageProcessing.identifyEnemy(enemyDict, imgGray)
                name = pokemonNameDict[int(fileNameOfClosestMatch[0:3])]
                print("The most likely enemy is " + name + " with accuracy of " + str(round(percentSure * 100, 2)) + "%")

                if percentSure < 0.5:
                    # Exits if it can't accurately identify the Pokemon 3 times
                    print("Unknown Enemy Pokemon")
                    exit(3)

        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find enemy")

        # If the enemy Pokemon is shiny,
        if imageProcessing.isShinyPokemon(fileNameOfClosestMatch):
            shl.shinySequence()
        else:
            # identify Run on screen
            while True:
                if shl.isImageFound("Run"):
                    break
                else:
                    print("...", end="")

            # Move mouse to Run location and click twice
            shl.clickScreen("Run", clickNum=2, waitTime=1)


def main():
    global totalEncountered

    # Populate a dictionary linking Pokemon name to number
    pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")

    # Ask the user which area type they will be hunting in
    # These correspond to the lists of wild Pokemon by area
    print("What area will you be shiny hunting in?")
    print("1: Walking in Grass")
    print("2: Walking in a Cave")
    print("3: Walking in a Building")
    print("4: Surfing (anywhere)")

    selection = int(input("Selection: "))

    while selection != 1 and selection != 2 and selection != 3 and selection != 4:
        print("\nThat selection was invalid\n")
        print("What area will you be shiny hunting in?")
        print("1: Walking in Grass")
        print("2: Walking in a Cave")
        print("3: Walking in a Building")
        print("4: Surfing (anywhere)")
        selection = int(input("Selection: "))

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

    selection = int(input("\nSelection: "))
    while selection < 1 or selection > len(areaList):
        print("\nThat selection was invalid\n")
        selection = int(input("Selection: "))

    # Get the specific area from the area type list
    selectionIndex = selection - 1
    huntingList = areaList[selectionIndex][1:]

    # Get a list of numbers corresponding to the names of Pokemon in the area
    huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, huntingList)

    # Get the folder name that's created, filled with reference images of Pokemon
    searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

    # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
    enemyDict = uploadImages.getImageDict(searchFolderName)

    totalEncountered = int(input("How many encounters have you had previously?: "))

    # Ask the user if they'd like to run up and down or left and right
    print("\nWould you like to run")
    print("1: Up and Down")
    print("2: Left and Right")
    selection = int(input("Selection: "))
    while selection != 1 and selection != 2:
        print("\nWould you like to run")
        print("1: Up and Down")
        print("2: Left and Right")
        selection = int(input("Selection: "))

    upDown = True
    if selection == 2:
        upDown = False

    # Final check to make sure the emulator is ready to be ran
    print("\nPlease make sure DeSmuMe is pulled up and your player is in " + areaList[selectionIndex][0])
    input("Press 'Enter' to continue ")

    # Run the emulator
    run(pokemonNameDict, enemyDict, upDown)


main()
