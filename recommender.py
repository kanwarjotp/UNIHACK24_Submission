##This is the basic foundational program##

import json #imports json module
import sklearn #imports scikit module (machine learning)

# Sample clothing data
clothing_data = [
    {"id": 1, "type": "Hat", "color": "Blue"},
    {"id": 2, "type": "Hat", "color": "LightBlue"},
    {"id": 3, "type": "Hat", "color": "Cat"},
    {"id": 4, "type": "Hat", "color": "Red"},
    {"id": 5, "type": "Hat", "color": "Yellow"},
    {"id": 6, "type": "Hat", "color": "Green"},
    {"id": 7, "type": "Hat", "color": "LightGreen"},
    {"id": 8, "type": "Hat", "color": "Orange"},
    {"id": 9, "type": "Hat", "color": "DarkGreen"},
    {"id": 10, "type": "Hat", "color": "Purple"},
    {"id": 11, "type": "Hat", "color": "Blue"},
    # Add more clothing items as needed
]

# This saves the data to a json file
with open("clothing_data.json", "w") as file:
    json.dump(clothing_data, file)

###############################################################################

#Parses the user's imput so the program can recognise info on the same line

def parse_input(input_string):
    parts = input_string.split('.')
    item_id = int(parts[0])
    item_type = parts[1]
    item_color = parts[2]
    liked = True if parts[3].lower() == 'yes' else False
    return item_id, item_type, item_color, liked

###############################################################################

user_preferences = {}

# ^^ empty Json file, v below is how we load it
try:
    with open("user_preferences.json", "r") as file:
        user_preferences = json.load(file)
except FileNotFoundError:
    pass

# A function that will update the userpreferences
def update_preferences(item_id, liked):
    user_preferences[item_id] = liked
    with open("user_preferences.json", "w") as file:
        json.dump(user_preferences, file)

###############################################################################

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

# Assigns RGB values to colors (color is one less letter than colour)
COLORS_RGB = {
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Blue': (0, 0, 255),
    'LightBlue': (173, 216, 230),
    'Cat': (0, 0, 139),
    'Purple': (128, 0, 128),
    'DarkGreen': (1, 50, 32),
    'LightGreen': (144, 238, 144),
    'Orange': (255, 165, 0),
    # Add more colors as needed
}

# Calculates colour similarity useing euclidean geometry (The distance between 2 3D vectors)
def color_similarity(color1, color2):
    color1_rgb = COLORS_RGB.get(color1, (0, 0, 0))  # Defaults to black if color not found
    color2_rgb = COLORS_RGB.get(color2, (0, 0, 0))
    distance = np.linalg.norm(np.array(color1_rgb) - np.array(color2_rgb))
    similarity = 1 / (1 + distance)
    return similarity

# This set retores the ids
recommended_item_ids = set()

###############################################################################

# Filters out previous reccommended items
def recommend_items(item_type, item_color, liked):
    global prev_recommended_item_id, recommended_item_ids

    relevant_items = [item for item in clothing_data if item['type'] == item_type]

    # Filter out items of disliked color
    if not liked:
        relevant_items = [item for item in relevant_items if item['color'] != item_color]

    similarities = [color_similarity(item['color'], item_color) for item in relevant_items]
    sorted_indices = np.argsort(similarities)[::-1]

    # Prioritises exact color matches, for example, will recomend another Blue Hat if availible
    recommended_items = [relevant_items[i] for i in sorted_indices if relevant_items[i]['color'] == item_color]

    if len(recommended_items) < 3:
        # Considers other colors if the reccommended item set is less than 3
        recommended_items += [relevant_items[i] for i in sorted_indices if relevant_items[i]['color'] != item_color][:3 - len(recommended_items)]

    if liked:
        recommended_items = [item for item in recommended_items if item['id'] not in user_preferences or user_preferences[item['id']]]
    else:
        recommended_items = [item for item in recommended_items if item['id'] not in user_preferences or not user_preferences[item['id']]]

    recommended_items = [item for item in recommended_items if item['id'] not in recommended_item_ids]

    # Selects the first item as a reccomendation
    recommended_item = recommended_items[0] if recommended_items else None

    if recommended_item:
        # updates the set of reccomended items
        recommended_item_ids.add(recommended_item['id'])
        return [recommended_item]
    else:
        # If the program finds nothing, returns None.None.None
        return [{"id": None, "type": None, "color": None}]

###############################################################################
###############################################################################

# Main program loop
while True:
    input_string = input("Please rate the clothing item (ID.Type.Color.Yes/No) or type 'exit' to quit: ")
    if input_string.lower() == 'exit': #Note this text ^ can be removed, its just for ease of use for now
        break

    item_id, item_type, item_color, liked = parse_input(input_string)

    recommended_items = recommend_items(item_type, item_color, liked)

    # Prints the recommended items to the user
    print("Recommended items:")
    for item in recommended_items:
        print(f"{item['id']}.{item['type']}.{item['color']}")

    # Records the preferences of the user
    update_preferences(item_id, liked)

