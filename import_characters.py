import json
import os
from fighter import Fighter
import pygame
from settings import *

def load_character_data(directory):
    characters = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                character_data = json.load(f)
                characters.append(character_data)
    return characters

def import_characters():
    character_directory = './Characters'
    character_data_list = load_character_data(character_directory)

    fighters = []

    for character_data in character_data_list:
       sprite_sheet = pygame.image.load(f'{character_directory}/Sprites/{character_data["sprite_sheet"]}').convert_alpha()
       thumbnail = pygame.image.load(f'{character_directory}/Sprites/{character_data["thumbnail"]}').convert_alpha()
       data = [character_data["name"], character_data["health"], character_data["stamina"], character_data["dmg1"], character_data["dmg2"]]
       fighter = Fighter(1, 200, 310, False, data, sprite_sheet, character_data["animation_steps"], thumbnail)
       fighters.append(fighter)

    return fighters

