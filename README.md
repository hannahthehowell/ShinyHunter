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
* Directories:
  * Anchor Images [link](#anchor-images-directory)
  * HGSS_AllSprites
  * TestingScreenshots
  * Search Images
  * WildPokemonLists
* Text files:
  * EggRoster.txt
* CSV files:
  * PokemonListByNumber.csv
* Python files:
  * getSprites.py

### Anchor Images Directory
This directory contains the cropped images (all .png) of buttons or other parts of the emulator that the script either uses to 
verify that it is the correct screen, or to click in cases like the 'Run' or 'Next' buttons. 
   * This is also used for finding the buttons needed for options like using the bike or running shoes.
   * Here is an example of the 'ShoesOn' anchor image:
   ![Shoes On image](/AnchorImages/ShoesOn.png "ShoesOn")

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

### EggRoster.txt
This text file has a list of each possible Pokémon that can be hatched in the game.
   * The text file is set up with each Pokémon listed on its own individual line 

### PokemonListByNumber.csv
This csv file is similar to the EggRoster.txt file, but instead it lists the Pokedex number, a comma, and then 
the Pokémon's name. 
   * This file is useful to look up Pokémon by their Pokedex number or to use the Pokedex number to find a Pokémon's name
   * Naming convention:
     * `<Pokedex #>,<Pokémon's name>,`

### getSprites.py
This python module uses several libraries to download all the needed sprite images from [pokencyclopedia](https://pokencyclopedia.info/). 
These sprites images are cropped, saved using their  unique id numbers (using information from the url) and placed in the 
correct path (currently "/Downloaded"). 
* The following libraries are required:
  * requests, shutil, BeautifulSoup imported from bs4 and urllib
* In the case of successfully running this a message is printed "Image successfully Downloaded" followed by the file
name and the images are properly saved.
* In the case of getting this error "Image Couldn't be retrieved" there was an issue with getting the image