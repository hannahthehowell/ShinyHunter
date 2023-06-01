# ShinyHunter
Script to hunt for Shiny Pokémon by processing screenshots of a Pokémon game on an emulator, and controlling the emulator

## Software Requirements
DeSmuME Nintendo DS emulator version 0.9.11. (Untested compatibility with latest version 0.9.13).

Pokémon HeartGold or SoulSilver ROM file.  Please acquire these file legally.

## Running
Please view the scripts running in these three videos:

Wild Hunting: https://drive.google.com/file/d/17Mhwu9mQmquz-my4zdbALuYNB0W3rfsC/view?usp=sharing

Egg Hatching: https://drive.google.com/file/d/1v7sH_eaBhdrUwpJpi1g3-R1YpIzkQCIh/view?usp=sharing

Hatching Full-odds Shiny Eevee: https://www.twitch.tv/roxa_bandita/clip/DrabSpunkyBasenjiCharlieBitMe-hQipg-YstDaOipri

---
***
___

## Table of Contents
* [Directories:](#directories)
  * [Anchor Images](#anchor-images-directory)
  * [HGSS_AllSprites](#hgss_allsprites-directory)
  * [TestingScreenshots](#testingscreenshots-directory)
  * [Search Images](#search-images-directory )
  * [WildPokemonLists](#wildpokemonlists-directory)
* [Text files:](#text-files)
  * [EggRoster.txt](#eggrostertxt)
* [CSV files:](#csv-files)
  * [PokemonListByNumber.csv](#pokemonlistbynumbercsv)
* [Python files:](#python-files)
  * [getSprites.py](#getspritespy)
  * [imageProcessing.py](#imageprocessingpy)
  * [main_egg.py](#main_eggpy)
  * [main_wild.py](#main_wildpy)
  * [ShinyHuntLib.py](#shinyhuntlibpy)
  * [uploadImages.py](#uploadimagespy)
  * [unit_tests.py](#unit_testspy)


## Directories:
### Anchor Images Directory
This directory contains the cropped images (all .png) of buttons or other parts of the emulator that the script either uses to 
verify that it is the correct screen, or to click in cases like the 'Run' or 'Next' buttons. 
   * This is also used for finding the buttons needed for options like using the bike or running shoes.
   * Here is an example of the 'ShoesOn' anchor image:
   ![Shoes On image](/AnchorImages/ShoesOn.PNG "ShoesOn")

### HGSS_AllSprites Directory
This directory contains the cropped images of each possible Pokémon sprite, and their variants. These variations can 
include things such as gender, elemental form, and shiny status. 
 * The naming convention is as follows:
   * `<Pokedex #>[.<Gender or Elemental Form>].<Animation Frame #>[.S]`
     * The first element is *required* and is the Pokémon's Pokedex number
     * The element is *optional* and is either the gender of the Pokémon (m or f) or the elemental form of the Pokémon
     * The third element is *required*, a number that indicates the animation frame that the screen was in as Pokémon can 
     at time have multiple possible animations (or stances)
     * The last element is an *optional* 'S' that is present in the sprite's name if the Pokémon is shiny
 * Example of a sprite named "250.1.S.png" (aka shiny Ho-oh):
 ![Shiny Ho oh](/HGSS_AllSprites/250.1.S.png "Shiny Ho oh")

### TestingScreenshots Directory
This directory contains three directories (each with screenshot .png files) and one .png file. The purpose of these 
testing screenshots is in testing to ensure that wild encounters will properly catch their targets. The files are split
into the following:
 * hatch:
   * This directory contains 5 examples of the hatching screen for Pokémon hatching including magikarp, onix and both regular
   and shiny rattata
 * lakeside:
   * This is the largest subdirectory of testing screenshots as it is used to maintain the ideal walking path.
     * The path avoids NPC encounters, grass, buildings and other obstructions. 
     * To maintain the path the screenshots checks:
       * If the player starting in the right position
       * If there is a new egg to be picked up (if hatching eggs)
         * If the old man NPC is facing left if he has an egg or down if he does not
   * The naming convention for the screenshots is as follows:
     * `[false]<lakeside #>.[left].<#>.png`
       * false is an *optional* parameter, and if there, it's false, otherwise it is true
       * lakeside is *required* in the name
       * left is *optional*,if present there is an egg to be picked up
       * the number is *required*, it corresponds to the time (24hr clock)
 * wild:
   * This directory is similar to hatch, but with a few more examples and for wild encounters with Pokémon, not for hatching

### Search Images Directory 
This directory is created and populated at runtime, so it won't initially be in the source folder upon set up. 
   * The images in this directory will be dynamically populated with the Pokémon sprites that are being hunted for.
     * In the case of hunting for shinies in the wild the desired location would be places like Route 29 or the Union
     Cave. All sprite images from these locations would then be populated into the Search Image directory.
     * In the case of hatching eggs the Search Image directory is populated with the Pokémon's possible sprites that can
     be hatched from the eggs in your inventory.

### WildPokemonLists Directory 
This directory contains four text files, each containing sets of a location followed by the Pokémon in that location, the 
next location has its own line.
   * The four text files are as follows:
     * HGSSWildPokemonListBuilding.txt
       * Lists all the locations inside of buildings and the respective Pokémon found there 
     * HGSSWildPokemonListCave.txt
       * Lists all the locations inside of caves and the respective Pokémon found there
     * HGSSWildPokemonListGrass.txt
       * Lists all the locations with grass (routes) and the respective Pokémon found there
     * HGSSWildPokemonListSurf.txt
       * Lists all the locations where you can surf and the respective Pokémon found there
   * The naming convention is as follows:
     * `<Location #><Pokémon's name>[Pokémon's name],[Pokémon's name],....`
   * Examples:
     * "Route 29, Pidgey, Sentret, Rattata, Hoothoot"
     * "Dark Cave, Magikarp"


## Text files:
### EggRoster.txt
This text file has a list of each possible Pokémon that can be hatched in the game.
   * The text file is set up with each Pokémon listed on its own individual line 


## CSV files:
### PokemonListByNumber.csv
This csv file is similar to the EggRoster.txt file, but instead it lists the Pokedex number, a comma, and then 
the Pokémon's name. 
   * This file is useful to look up Pokémon by their Pokedex number or to use the Pokedex number to find a Pokémon's name
   * Naming convention:
     * `<Pokedex #>,<Pokémon's name>,`


## Python files:
### main_wild.py
This module is responsible for hunting Pokémon in the wild. In order to do this the module handles the initial set up for
the shiny hunting loop by getting three parameters: the Pokémon name dictionary, the enemy dictionary and the up/down or
left/right decision for the hunt. This user input for the location of the hunt is then used by the ShinyHuntLib module to
get the screenshots for the possibly hunted Pokémon in that area. This new list of possible Pokémon is then placed into 
the area list. Using this new area list the user is given options to pick their route for shiny hunting and an option to 
set the encounter count, if desired. During the running of this module the ROM is reset every ~180 seconds to avoid very
slow resets. When a Pokémon is found, the emulator is paused and a message (and optional beep sound) is displayed.

### main_egg.py
This module is very similar to the main_wild.py module, but instead of looking for Pokémon in places like the routes and 
caves, this module handles shiny hunting by hatching eggs. Once the user inputs the name of the Pokémon that is getting 
hatched, then the Pokémon dictionary and egg roster can be updated. This allows for the directory of sprite images can 
be filled with the correct shiny (and its variants) for comparing. Also included in these checks is seeing if the user is
using, or wants to use a bike or running shoes. Both cannot be used at the same time, screenshots are used to verify the
users input to ensure continuity of the program. A warning is also displayed letting the user know that any 'extra' Pokémon,
besides the one required Pokémon in your party (usually with an ability to hatch eggs faster), in their party will be
permanently lost. 

Several checks are preformed in order to ensure that the path taken by the character is 'safe' from obstacles, NPCs and 
wild encounters. Checks are also made to see if the player is starting their egg hatching from the right location as well
as checking to see if there are new eggs to be picked up or non-shiny Pokémon to be discarded. 

### getSprites.py
This module uses several libraries to download all the needed sprite images from [pokencyclopedia](https://pokencyclopedia.info/). 
These sprites images are cropped, saved using their  unique id numbers (using information from the url) and placed in the 
correct path (currently "/Downloaded"). 
* The following libraries are required:
  * requests, shutil, BeautifulSoup imported from bs4 and urllib
* In the case of successfully running this a message is printed "Image successfully Downloaded" followed by the file
name and the images are properly saved.
* In the case of getting this error "Image Couldn't be retrieved" there was an issue with getting the image

### imageProcessing.py
This module contains several functions that are used to check images in the form of either screenshots from the emulator, 
testing screenshots or the sprite images. Some of these functions include identifying the enemy's Pokémon or identifying
the Pokémon that just hatched. Other functions include checking to see which direction the man is facing by the river 
(which tells indicates if there is an egg ready to be picked up or not) or checking if the player is in the right 
location by the Lakeside. More functions included are checking if the Pokémon is shiny and removing the background's color
from hatched eggs' screenshots to make them easier to compare. 

### ShinyHuntLib.py
This module handles several of the necessary functions for the Desmume emulator and it's uses. These functions include 
checking that the emulator is up and running, that an image was found, clicking on a specific image on the screen, taking 
or removing screenshots, a sequence that gets played when a shiny is found and a function to reset the ROM. Resetting the 
ROM occasionally (every ~180 seconds) is important to ensure that it does not slow down or freeze up. 

### uploadImages.py

### unit_tests.py
