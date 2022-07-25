import unittest
import cv2
import uploadImages
import imageProcessing
import ShinyHuntLib


class TestUser(unittest.TestCase):
    def testAllWildLists(self):
        pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
        listStrings = ["WildPokemonLists/HGSSWildPokemonListGrass.txt",
                       "WildPokemonLists/HGSSWildPokemonListCave.txt",
                       "WildPokemonLists/HGSSWildPokemonListBuilding.txt",
                       "WildPokemonLists/HGSSWildPokemonListSurf.txt"]
        for listString in listStrings:
            areaList = uploadImages.loadList(listString)
            for area in areaList:
                # print(area[0])
                huntingList = area[1:]
                huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, huntingList)
                # print(huntingNumbers)

    def test_shiny_wild_true(self):
        list_of_wild_shiny = [
            "abra",
            "drowzee",
            "oddish",
            "onix",
            "paras",
            "rattata",
            "sandshrew"
        ]
        for mon in list_of_wild_shiny:
            pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
            # Get a list of numbers corresponding to the names of Pokemon in the area
            huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, [mon.title()])

            # Get the folder name that's created, filled with reference images of Pokemon
            searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

            # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
            enemyDict = uploadImages.getImageDict(searchFolderName)

            path = "TestingScreenshots/wild/wild_" + mon + "_shiny.png"
            imgGray = cv2.imread(path, 0)

            fileNameOfClosestMatch, percentSure = imageProcessing.identifyEnemy(enemyDict, imgGray)
            name = pokemonNameDict[int(fileNameOfClosestMatch[0:3])]
            print("The most likely enemy is " + name + " with accuracy of " + str(round(percentSure * 100, 2)) + "%")
            self.assertTrue(imageProcessing.isShinyPokemon(fileNameOfClosestMatch))

    def test_shiny_wild_false(self):
        list_of_wild = [
            "abra",
            "drowzee",
            "rattata",
            "sandshrew",
            "zubat"
        ]
        for mon in list_of_wild:
            pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
            # Get a list of numbers corresponding to the names of Pokemon in the area
            huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, [mon.title()])

            # Get the folder name that's created, filled with reference images of Pokemon
            searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

            # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
            enemyDict = uploadImages.getImageDict(searchFolderName)

            path = "TestingScreenshots/wild/wild_" + mon + ".png"
            imgGray = cv2.imread(path, 0)

            fileNameOfClosestMatch, percentSure = imageProcessing.identifyEnemy(enemyDict, imgGray)
            name = pokemonNameDict[int(fileNameOfClosestMatch[0:3])]
            print("The most likely enemy is " + name + " with accuracy of " + str(round(percentSure * 100, 2)) + "%")
            self.assertFalse(imageProcessing.isShinyPokemon(fileNameOfClosestMatch))

    def test_shiny_egg_true(self):
        list_of_hatch_shiny = [
            "onix",
            "rattata"
        ]
        for mon in list_of_hatch_shiny:
            pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
            # Get a list of numbers corresponding to the names of Pokemon in the area
            huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, [mon.title()])

            # Get the folder name that's created, filled with reference images of Pokemon
            searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

            # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
            hatchDict = uploadImages.getImageDict(searchFolderName)

            # Reads in colors in BGR
            path = "TestingScreenshots/hatch/hatch_" + mon + "_shiny.png"
            imgColor = cv2.imread(path, 1)

            imageProcessing.removeEggBackground(imgColor)
            imgGray = cv2.imread("Screenshot.png", 0)

            fileNameOfClosestMatch = imageProcessing.identifyHatched(hatchDict, imgGray)

            self.assertTrue(imageProcessing.isShinyPokemon(fileNameOfClosestMatch))

    def test_shiny_egg_false(self):
        list_of_hatch_shiny = [
            "onix",
            "rattata",
            "magikarp"
        ]
        for mon in list_of_hatch_shiny:
            pokemonNameDict = uploadImages.loadDict("PokemonListByNumber.csv")
            # Get a list of numbers corresponding to the names of Pokemon in the area
            huntingNumbers = uploadImages.listToNumbers(pokemonNameDict, [mon.title()])

            # Get the folder name that's created, filled with reference images of Pokemon
            searchFolderName = uploadImages.createAndFillSearchFolder(huntingNumbers)

            # Create a dictionary of possible enemies and their numbers based on the newly created and filled folder
            hatchDict = uploadImages.getImageDict(searchFolderName)

            # Reads in colors in BGR
            path = "TestingScreenshots/hatch/hatch_" + mon + ".png"
            imgColor = cv2.imread(path, 1)

            imageProcessing.removeEggBackground(imgColor)
            imgGray = cv2.imread("Screenshot.png", 0)

            fileNameOfClosestMatch = imageProcessing.identifyHatched(hatchDict, imgGray)

            self.assertFalse(imageProcessing.isShinyPokemon(fileNameOfClosestMatch))

    def test_man_facing_left(self):
        nums = ["0", "2", "4", "8", "11", "15", "17", "19", "23"]
        # facing down pics
        for num in nums:
            path = "TestingScreenshots/lakeside/lakeside-" + num + ".png"
            imgGray = cv2.imread(path, 0)
            self.assertFalse(imageProcessing.manFacingLeft(imgGray))

        # facing left pics
        for num in nums:
            path = "TestingScreenshots/lakeside/lakeside-left-" + num + ".png"
            imgGray = cv2.imread(path, 0)
            self.assertTrue(imageProcessing.manFacingLeft(imgGray))

    def test_is_lakeside(self):
        nums = ["0", "2", "4", "8", "11", "15", "17", "19", "23"]
        # facing down pics
        for num in nums:
            path = "TestingScreenshots/lakeside/lakeside-" + num + ".png"
            imgGray = cv2.imread(path, 0)
            self.assertTrue(imageProcessing.isAtLakeside(imgGray))

        # facing left pics
        for num in nums:
            path = "TestingScreenshots/lakeside/lakeside-left-" + num + ".png"
            imgGray = cv2.imread(path, 0)
            self.assertTrue(imageProcessing.isAtLakeside(imgGray))

        # not at lakeside pics
        for i in range(1, 6+1):
            path = "TestingScreenshots/lakeside/false_lakeside_" + str(i) + ".png"
            imgGray = cv2.imread(path, 0)
            self.assertFalse(imageProcessing.isAtLakeside(imgGray))


if __name__ == '__main__':
    unittest.main()
