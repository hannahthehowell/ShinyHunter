import uploadImages
import imageProcessing
import ShinyHuntLib as shl

import cv2
import time
import pyautogui


singleTileMovement = 0.018
singleTilePause = 0.3


totalHatched = 0  # TODO Replace 0 with how many previous hatches

hatchDict = {}
numEggsInParty = 0
numHatchedInParty = 0
hasBike = False


# Used to move the player in any direction any amount of times
def moveNumTiles(key, num=1):
    for i in range(num):
        time.sleep(singleTilePause)
        pyautogui.keyDown(key)
        time.sleep(singleTileMovement)
        pyautogui.keyUp(key)
        if shl.isImageFound("Oh"):
            hatchingSequence()


# Used to go through a door
def goThroughDoor(key):
    pyautogui.keyDown(key)
    time.sleep(singleTileMovement*7)
    pyautogui.keyUp(key)
    time.sleep(singleTilePause*12)
    if shl.isImageFound("Oh"):
        hatchingSequence()


# Used to move the player from the daycare door to the lakeside
def moveToEggStart():
    # Go into Daycare then leave
    goThroughDoor('w')
    goThroughDoor('s')

    # Move from door to lakeside 8 tiles left
    moveNumTiles('a', 8)

    # Take screenshot and determine if in correct spot
    imgGray = shl.getScreenshot()
    if not imageProcessing.isAtLakeside(imgGray):
        print("It appears that you are in an incorrect location")
        exit(1)


# Used when an egg is hatching
def hatchingSequence():
    global numHatchedInParty
    global totalHatched

    # Identify A Next on screen
    shl.clickScreen("ANext")

    time.sleep(12)

    imgGray = shl.getScreenshot()
    fileNameOfClosestMatch = imageProcessing.identifyHatched(hatchDict, imgGray)
    if imageProcessing.isShinyPokemon(fileNameOfClosestMatch):
        shl.shinySequence()

    totalHatched += 1
    print("Hatching egg number", totalHatched)

    # Identify No on screen
    shl.clickScreen("No")

    time.sleep(5)
    numHatchedInParty += 1


# Used when the party is full of unhatched eggs
def partyFullAndNotHatched():
    global numHatchedInParty

    # Hatch full party of eggs
    while numHatchedInParty < 5:
        if hasBike:
            time_len = 2
        else:
            time_len = 3

        # Go up to top
        i = 0
        while i < time_len:
            # Go up
            pyautogui.keyDown('w')
            time.sleep(3.5)
            pyautogui.keyUp('w')

            # Check if hatching
            if shl.isImageFound("Oh"):
                hatchingSequence()
            else:
                i += 1

        # Go down to lake
        i = 0
        while i < time_len:
            # Go down
            pyautogui.keyDown('s')
            time.sleep(3.5)
            pyautogui.keyUp('s')

            # Check if hatching
            if shl.isImageFound("Oh"):
                hatchingSequence()
            else:
                i += 1


# Used to move the player to pick up an egg and return to the lakeside area
def pickupEggAndReturn():
    global numEggsInParty

    # move up 1 tile, right 4 tiles
    moveNumTiles('w', 1)
    moveNumTiles('d', 4)

    # Identify ATalk on screen
    shl.clickScreen("ATalk", clickNum=5, waitTime=1.5)

    # Identify YES on screen
    shl.clickScreen("YesPickup", waitTime=6)

    # Identify ANext on screen
    shl.clickScreen("ANext")

    # walk left 4 tiles
    moveNumTiles('a', 4)

    numEggsInParty += 1


# Used to move the player from the lakeside to the PC in the daycare
def moveFromLakesideToPC():
    # walk tiles right 8 and up 1
    moveNumTiles('d', 8)
    goThroughDoor('w')
    # walk tiles left then up
    moveNumTiles('a', 2)
    moveNumTiles('w', 4)


# Used to move the player from the PC in the daycare to the lakeside
def moveFromPCToLakeside():
    # move right 2 tiles, move down 5 tiles
    moveNumTiles('d', 2)
    moveNumTiles('s', 4)
    # go down door, walk tiles left 8
    goThroughDoor('s')
    moveNumTiles('a', 8)


# Used to release the 2nd party member in the PC
def release2ndPartyMember(left, width, top):
    # Move mouse to image name -94 px up
    pyautogui.moveTo(x=(left + width), y=(top - 94))

    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()

    time.sleep(0.5)

    # Click release
    shl.clickScreen("Release", waitTime=0.5)

    # Click yes
    shl.clickScreen("YesRelease", waitTime=1.5)

    # Move mouse to image name -94 px up and click 2x
    pyautogui.moveTo(x=(left + width), y=(top - 94))
    for j in range(2):
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.mouseUp()
        time.sleep(0.5)


# Used to boot up the PC, release 5 party Pokemon, then shutdown the PC
def release5Pokemon():
    global numEggsInParty
    global numHatchedInParty

    # ACheck
    shl.clickScreen("ACheck", waitTime=1)

    # ANext 1 time
    shl.clickScreen("ANext", waitTime=1)

    # Someone's or Bill's PC
    if shl.isImageFound("Someones_PC"):
        shl.clickScreen("Someones_PC", waitTime=1)
    else:
        shl.clickScreen("Bills_PC", waitTime=1)

    # hit bottom screen anywhere
    shl.clickScreen("bottom_screen")

    # click Move Pokemon
    shl.clickScreen("MovePokemon", waitTime=1.5)

    # click Party Pokemon
    shl.clickScreen("Party", waitTime=1)

    # Find "switch"
    try:
        left, top, width, height = pyautogui.locateOnScreen("AnchorImages/Switch.png")
    except (pyautogui.ImageNotFoundException, TypeError):
        print("Could not find SWITCH on the screen")
        exit(1)

    # release 2nd party member 5 times
    for i in range(5):
        release2ndPartyMember(left, width, top)

    # click exit
    shl.clickScreen("Exit_PC", waitTime=1)

    # Return from box
    shl.clickScreen("Return", waitTime=1)

    # Yes, exit the box
    shl.clickScreen("YesExit", waitTime=2)

    # see ya
    shl.clickScreen("Seeya", waitTime=1)

    # switch off
    shl.clickScreen("SwitchOff", waitTime=1)

    numEggsInParty = 0
    numHatchedInParty = 0


# Used to move the player down to the lakeside position
def moveToLakeside():
    imgGray = shl.getScreenshot()
    while not imageProcessing.isAtLakeside(imgGray):
        if shl.isImageFound("Oh"):
            hatchingSequence()
        else:
            pyautogui.keyDown('s')
            time.sleep(2)
            pyautogui.keyUp('s')
            imgGray = shl.getScreenshot()


# Used to move the player up to the top of Goldenrod then down to the lakeside, once
def goUpAndDownOnce():
    if hasBike:
        time_len = 2
    else:
        time_len = 4

    # Go up to top
    i = 0
    while i < time_len:
        # Go up
        pyautogui.keyDown('w')
        time.sleep(3.5)
        pyautogui.keyUp('w')

        # Check if hatching
        if shl.isImageFound("Oh"):
            hatchingSequence()
        else:
            i += 1

    # Go down to lake
    i = 0
    while i < time_len:
        # Go down
        pyautogui.keyDown('s')
        time.sleep(3.5)
        pyautogui.keyUp('s')

        # Check if hatching
        if shl.isImageFound("Oh"):
            hatchingSequence()
        else:
            i += 1


##################################################################################################

# Used to run the emulator using PyAutoGUI
def run():
    global hasBike
    global numHatchedInParty
    global numEggsInParty

    shl.removeScreenshot()

    # Identify Desmume on screen via the options button and click
    shl.identifyDeSmuME()

    # Identify bike on hotbar if selected
    if hasBike:
        if not shl.isImageFound("bike"):
            print("Could not find your bike")
            hasBike = False
    shl.clickScreen("ShoesOn", fatal=False)

    # Move from outside the daycare door to the starting position by the lake
    moveToEggStart()

    # Turn on bike and running shoes off OR running shoes on
    if hasBike:
        # Identify Shoes On on screen
        shl.clickScreen("ShoesOn", fatal=False)
        shl.clickScreen("bike")
    else:
        # Identify Shoes Off on screen
        shl.clickScreen("ShoesOff", fatal=False)

    # Master while loop - only exits if it finds a shiny Pokemon
    hatching = True
    while hatching:
        # If party if not full of eggs
        if numEggsInParty < 5:
            # Move down to lakeside
            moveToLakeside()

            # If man facing left
            imgGray = cv2.imread("Screenshot.png", 0)

            if imageProcessing.manFacingLeft(imgGray):
                if hasBike:
                    # Turn off bike
                    shl.clickScreen("bike")
                else:
                    # Turn off shoes
                    shl.clickScreen("ShoesOn")

                # Pick up egg and return to lakeside
                pickupEggAndReturn()

                if hasBike:
                    # Turn on bike
                    shl.clickScreen("bike")
                else:
                    # Turn on bike
                    shl.clickScreen("ShoesOff")

            # Go up and down once
            goUpAndDownOnce()

        # If party is full but not all hatched, loop until all hatched
        if numEggsInParty >= 5 and numHatchedInParty < 5:
            partyFullAndNotHatched()

        # If party is full of hatched pokemon
        if numEggsInParty >= 5 and numHatchedInParty >= 5:
            # Move down to lakeside
            moveToLakeside()

            # Turn off bike
            if hasBike:
                shl.clickScreen("bike")
            else:
                # Identify Shoes On on screen
                shl.clickScreen("ShoesOn")

            # Move into daycare
            moveFromLakesideToPC()

            # Release sequence
            release5Pokemon()

            # Get back to lakeside
            moveFromPCToLakeside()

            if hasBike:
                # Turn on bike
                shl.clickScreen("bike")
            else:
                # Turn on shoes
                shl.clickScreen("ShoesOff")


def main():
    global hatchDict
    global hasBike

    # Populate a dictionary linking Pokemon name to number
    pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
    # Populate roster of possible pokemon in egg
    eggRoster = set(open("EggRoster.txt").read().splitlines())

    selectionValid = False
    while not selectionValid:
        # Ask the user which species they will hatching
        print("What Pokemon will be hatching from the eggs?")
        selection = input("Hatching: ").title()
        if selection in eggRoster:
            selectionValid = True
        elif selection == "Farfetch'D":
            selectionValid = True
            selection = "Farfetch'd"
        else:
            print("\nThat selection was invalid")
            print("Please write the name of the Pokemon that will hatch, not necessarily the Pokemon you are breeding\n")

    # Get a list of numbers corresponding to the names of Pokemon in the area
    huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, [selection])

    # Get the folder name that's created, filled with reference images of Pokemon
    searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

    # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
    hatchDict = uploadImages.getImageDict(searchFolderName)

    # Ask the user if they'd like to use a bike
    selection = 0
    while selection != 1 and selection != 2:
        print("\nWould you like to use your bike?")
        print("1: Yes")
        print("2: No")
        selection = int(input("Selection: "))

    if selection == 1:
        hasBike = True
        print("Please have your bike registered on your bottom screen")

    # Final check to make sure the emulator is ready to be ran
    print("\nPlease make sure DeSmuMe is pulled up and your player is on the tile immediately outside the daycare door")
    print("Please also make sure your party ONLY has 1 Pokemon in it (preferably with Flame Body ability)")
    print("\n***WARNING: This code will release all non-shiny Pokemon that hatch from eggs and any additional party members***")
    agree = input("\nPlease type the word 'agree' if you understand. Type anything else to cancel: ")
    if agree == 'agree':
        # Run the emulator
        run()
    else:
        print("Cancelling emulation")
        exit(1)


main()
