import uploadImages
import imageProcessing

import cv2
import time
import winsound
import pyautogui


def main():
    pokemonNameDict = uploadImages.loadDict()

    folderStringAlly = "training_sprites_ally"
    trainingDictAlly = uploadImages.getTrainingDict(folderStringAlly)

    folderStringEnemy = "training_sprites_enemy"
    trainingDictEnemy = uploadImages.getTrainingDict(folderStringEnemy)

    folderStringTest = "testing_images_grass"
    # folderStringTest = "testing_images_cave"

    # folderStringTest = "testing_images_path"
    # folderStringTest = "testing_images_buildings"
    # folderStringTest = "advanced_testing"

    # folderStringTest = "testing_images_shiny"

    testingSetRGB = uploadImages.getTestingList(folderStringTest)
    testingListGray = uploadImages.makeListGray(testingSetRGB)

    for i in range(len(testingSetRGB)):
        imgRGB = testingSetRGB[i]
        imgGray = testingListGray[i]

        startTime = time.time()
        allyNumber = imageProcessing.identifyAlly(pokemonNameDict, trainingDictAlly, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find ally")

        startTime = time.time()
        enemyNumber = imageProcessing.identifyEnemy(pokemonNameDict, trainingDictEnemy, imgGray)
        endTime = time.time()
        print(round(endTime - startTime, 5), "seconds to find enemy")

        imageProcessing.identifyAllPokemon(pokemonNameDict, imgRGB, imgGray, trainingDictAlly, allyNumber, trainingDictEnemy, enemyNumber)

        if imageProcessing.isShinyEnemy(enemyNumber):
            print("IT'S SHINY")
            # while True:
            #     print("IT'S SHINY")
            #     winsound.Beep(2000, 100)
            #     time.sleep(2)

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
