import cv2
import numpy as np
import os
import csv
from matplotlib import pyplot as plt
import math
import random


def get_training_dict():
    image_set = {}
    for filename in os.listdir("training_sprites"):
        path = "training_sprites/" + filename
        im = cv2.imread(path, 0)
        imc = crop_bw_img(im)
        image_set[float(filename.strip(".png"))] = imc
    return image_set


def get_testing_set(folderString):
    image_set = []
    for filename in os.listdir(folderString):
        im = cv2.imread(os.path.join(folderString, filename))
        image_set.append(im)
    return image_set


def make_set_bw(image_set):
    bw_set = []
    for image in image_set:
        bw_set.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    return bw_set


def load_dict():
    input_file = csv.reader(open("PokemonListByNumber.csv", "r"))
    dictionary = {}
    for row in input_file:
        number, name = row
        dictionary[int(number)] = name
    return dictionary


# def crop_img(img):
#     color, width, height = img.shape[::-1]
#
#     topIndex = height - 1
#     bottomIndex = 0
#     leftIndex = width - 1
#     rightIndex = 0
#
#     white = [255, 255, 255]
#
#     for row in range(height):
#         for col in range(width):
#             if all(img[row][col] != white):
#                 if row < topIndex:
#                     topIndex = row
#                 if row > bottomIndex:
#                     bottomIndex = row
#                 if col < leftIndex:
#                     leftIndex = col
#                 if col > rightIndex:
#                     rightIndex = col
#
#     crop = img[topIndex:bottomIndex+1, leftIndex:rightIndex+1]
#
#     # plt.subplot(121),
#     # plt.imshow(img)
#     # plt.title('Original Image'),
#     # plt.xticks([]), plt.yticks([])
#     # plt.subplot(122),
#     # plt.imshow(crop)
#     # plt.title('Cropped Image'),
#     # plt.xticks([]), plt.yticks([])
#     # plt.show()
#
#     return crop


def crop_bw_img(img):
    width, height = img.shape[::-1]

    topIndex = height - 1
    bottomIndex = 0
    leftIndex = width - 1
    rightIndex = 0

    white = 255
    black = 0

    for row in range(height):
        for col in range(width):
            if img[row][col] != white:
                if row < topIndex:
                    topIndex = row
                if row > bottomIndex:
                    bottomIndex = row
                if col < leftIndex:
                    leftIndex = col
                if col > rightIndex:
                    rightIndex = col

    crop = img[topIndex:bottomIndex+1, leftIndex:rightIndex+1]

    width, height = crop.shape[::-1]

    for row in range(height):
        for col in range(width):
            if crop[row][col] == white:
                crop[row][col] = 128

    return crop


def identify_all_pokemon(pokemon_name_dict, training_dict_bw, img_rgb, img_gray):
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 1
    color = (255, 255, 255)
    thickness = 1

    for key in training_dict_bw:
        template = training_dict_bw[key]

        w, h = template.shape[::-1]

        # crop = img[topIndex:bottomIndex + 1, leftIndex:rightIndex + 1]
        portion = img_gray[0:192+1, 0:256+1]

        res = cv2.matchTemplate(portion, template, cv2.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        ''' When Black - 0.78 is where Chikorita false positive disappears; Weedle isn't found after 0.75 '''
        ''' When white - 0.95 gets most light pokemon'''
        if max_val > 0.96:  # TODO
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv2.rectangle(img_rgb, top_left, bottom_right, (255, 0, 0), 1)
            name = pokemon_name_dict[math.floor(key)]
            img_rgb = cv2.putText(img_rgb, name, top_left, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow("", img_rgb)


def identify_enemy(pokemon_name_dict, training_dict_bw, img_gray):
    ''' Test images are 384 x 256 '''
    ''' 152, 15 is top left '''
    ''' 231, 94 is bottom right '''
    tuples = []

    for key in training_dict_bw:
        template = training_dict_bw[key]

        # crop = img[topIndex:bottomIndex + 1, leftIndex:rightIndex + 1]
        portion = img_gray[15:94+1, 152:231+1]

        res = cv2.matchTemplate(portion, template, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        number = math.floor(key)
        tuples.append([number, max_val])

    highestIndex = 0
    highestVal = tuples[0][1]
    for i in range(len(tuples)):
        currentValue = tuples[i][1]
        if currentValue > highestVal:
            highestIndex = i
            highestVal = currentValue

    number = tuples[highestIndex][0]
    value = tuples[highestIndex][1]

    name = pokemon_name_dict[number]

    print("The most likely enemy is " + name + " with accuracy of " + str(round(value * 100, 2)) + "%")

    if name == "Metapod":  # TODO
        for i in range(len(tuples)):
            print(tuples[i])

    return number


def is_shiny_enemy(enemyNumber, img_rgb, img_gray):
    ''' Test images are 384 x 256 '''
    ''' 152, 15 is top left '''
    ''' 231, 94 is bottom right '''
    return False


def main():
    pokemon_name_dict = load_dict()

    training_dict_bw = get_training_dict()

    folderString = "testing_images_grass"
    # folderString = "testing_images_cave"
    testing_set_rgb = get_testing_set(folderString)
    testing_set_bw = make_set_bw(testing_set_rgb)

    for i in range(len(testing_set_rgb)):
        img_rgb = testing_set_rgb[i]
        img_gray = testing_set_bw[i]

        identify_all_pokemon(pokemon_name_dict, training_dict_bw, img_rgb, img_gray)
        enemyNumber = identify_enemy(pokemon_name_dict, training_dict_bw, img_gray)
        if is_shiny_enemy(enemyNumber, img_rgb, img_gray):
            print("IT'S SHINY")
        cv2.waitKey()

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
    # img2 = training_dict_bw[19]
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
