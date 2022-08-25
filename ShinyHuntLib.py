import cv2
from datetime import datetime
import os
import pyautogui
import time
import winsound


# Used to identify Desmume on screen via the options button
def identifyDeSmuME():
    try:
        left, top, width, height = pyautogui.locateOnScreen("AnchorImages/Options.png")
    except (pyautogui.ImageNotFoundException, TypeError):
        print("Could not find DeSmuMe on the screen")
        exit(1)

    # Move mouse to Desmume location and click
    pyautogui.click(x=left, y=(top + height + 5))


# Used to identify an imageName on screen
def isImageFound(imageName):
    try:
        path = "AnchorImages/" + imageName + ".png"
        left, top, width, height = pyautogui.locateOnScreen(path)
    except (pyautogui.ImageNotFoundException, TypeError):
        return False
    return True


# Used to click the screen on a specific image
def clickScreen(imageName, fatal=True, clickNum=1, waitTime=0):
    # Identify imageName on screen and click it
    try:
        path = "AnchorImages/" + imageName + ".png"
        left, top, width, height = pyautogui.locateOnScreen(path)
    except (pyautogui.ImageNotFoundException, TypeError):
        if fatal:
            print("Unable to find " + imageName + " button on screen")
            exit(1)
        else:
            return

    # Move mouse to image name and click x times
    pyautogui.moveTo(x=(left + width / 2), y=(top + height / 2))
    for i in range(clickNum):
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.mouseUp()

        time.sleep(waitTime)

    return True


# Used to take and save a screenshot
def getScreenshot(color=False):
    removeScreenshot()
    time.sleep(1)
    # Take screenshot - F12
    pyautogui.keyDown('f12')
    pyautogui.keyUp('f12')

    # Rename to "Screenshot"
    pyautogui.write("Screenshot")
    pyautogui.press('enter')
    time.sleep(2)

    if color:
        img = cv2.imread("Screenshot.png", 1)  # in BGR
    else:
        img = cv2.imread("Screenshot.png", 0)

    return img


# Remove testing screenshot if it already exists
def removeScreenshot():
    if os.path.exists("Screenshot.png"):
        os.remove("Screenshot.png")


# What to do if find a shiny
def shinySequence():
    # If the enemy Pokemon is shiny,
    clickScreen("Pause")

    print("IT'S SHINY")
    print(datetime.now())
    exit(5)  # Toggle comment on this line to exit or beep
    while True:
        winsound.Beep(2000, 100)
        time.sleep(0.75)


# Resets the ROM to keep the time low and saves quick
def resetROM():
    # locate place to click through credits
    try:
        leftO, topO, widthO, heightO = pyautogui.locateOnScreen("AnchorImages/Options.png")
    except (pyautogui.ImageNotFoundException, TypeError):
        exit(1)

    # reset ROM
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('r')
    pyautogui.keyUp('r')
    pyautogui.keyUp('ctrl')

    # click until you find Options
    while True:
        if isImageFound("Options"):
            break
        else:
            pyautogui.moveTo(x=(leftO - widthO / 2), y=(topO - heightO))
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.mouseUp()
