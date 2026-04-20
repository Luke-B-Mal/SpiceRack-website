import pandas as pd
import requests
import os
import time

# !!!!! REMOVE BEFORE ADD OR COMMIT, OR ESPECIALLY PUSH !!!!!
API_KEY = YOUR_API_KEY
CX = YOUR_CX
SAVE_FOLDER = "recipe_images"

#creates the file for the images in the current directory if it doesnt exist.
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def get_image(query):
    #compiles the api key and cx value into an api request with the paramets serving as ways to specify what I want.
    image_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": CX,
        "key": API_KEY,
        "searchType": "image", #only images
        "num": 1, #only one image downloaded (the first one)
        "imgSize": "medium", #do not want to make the dataframe too large
        "safe": "active" #doesnt make a difference whether on or off, but is needed.
    }

    try:
        #allows the program to try the request and catch an error instead of crashing.
        response = requests.get(image_url, params=params)
        response.raise_for_status()
        data=response.json()

        if "items" in data:
            return data["items"][0]["link"]
        
    except Exception as e:
        print(f"Error searching for {query}: {e}")
    return None

# if the request was successful, downloads the image from the pulled url.
def download_image(url, filename):
    try:
        image_data = requests.get(url, timeout=10).content #tries for ten seconds to pull the image.
        with open(os.path.join(SAVE_FOLDER, filename), "wb") as handler:
            handler.write(image_data)
        return True
    #catches the error if it doesnt work
    except Exception as e:
        print(f"Error downloading from {url}: {e}")
        return False

titles = pd.read_csv("data gather/clustered_recipes_sample1000.csv")['title'][0:100] #first hundred to not cause error when rate limit reached.

#acutal program that goes through the names and downloades them if it works.
for title in titles:
    image_url = get_image(title)

    #quick check to clean up the file names.
    file_name_li = []
    if image_url:
        for x in title:
            if x.isalnum() or x in "._- ":
                file_name_li.append(x)
    file_name = "".join(file_name_li).strip() + ".jpg"

    success = download_image(image_url, filename=file_name)
    if success:
        print(f"downloaded {file_name}")
