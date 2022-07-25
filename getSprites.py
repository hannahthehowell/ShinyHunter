"""
Run this script to download all of the HGSS front sprites
"""
# Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
from bs4 import BeautifulSoup  # to get html
import urllib  # to get url


site = "https://www.pokencyclopedia.info"
list_of_ext = [
    "/en/index.php?id=sprites/gen4/spr_hgss",
    "/en/index.php?id=sprites/gen4/spr_hgss_shiny"
]

# For each of the two extensions
for ext in list_of_ext:
    # Open the url, get the html
    u = urllib.request.urlopen(site + ext)
    soup = BeautifulSoup(u, features="lxml")

    # Get all the img src on the page
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))

    images = [i[2:] for i in images]

    # Remove any images that don't begin with 'sprites'
    clean_images = []
    for image in images:
        if image.startswith("/sprites/"):
            clean_images.append(image)

    # Upload each image
    for img in clean_images:
        image_url = site + img

        # Set up the image filename
        filename = img.split("/")[-1]
        filename = filename.split(".")[:-1]
        filename_list = filename[0].split("_")

        ufilename = ""
        for p in range(2, len(filename_list)):
            ufilename += filename_list[p] + "."
        if filename_list[1].endswith("-S"):
            ufilename += "S."
        ufilename += "png"

        finalFileName = "Downloaded/" + ufilename
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb permission.
            with open(finalFileName, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print("Image successfully Downloaded: ", finalFileName)
        else:
            print("Image Couldn't be retrieved")
