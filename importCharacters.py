import json
import os

def load_character_data(directory):
    characters = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                character_data = json.load(f)
                characters.append(character_data)
    return characters
