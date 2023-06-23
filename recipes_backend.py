from typing import List, Dict
import json


class Recipe:
    def __init__(self, name: str, ingredients: List[str], preparation: str):
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation

def load_recipes_from_json(path:str) -> Dict:
    """
    Loads a dictionary of Recipe objects from a json file
    :param path: the location of the json file
    :return: Dict. A dictionary containing Recipe objects
    """
    recipes = {}
    with open(path, "r", encoding='utf-8') as recipes_data:
        recipes_json = json.load(recipes_data)
        for entry in recipes_json:
            name = recipes_json[entry]['name']
            ingredients = recipes_json[entry]['ingredients']
            preparation = recipes_json[entry]['preparation']
            recipes[name] = Recipe(name, ingredients, preparation)
    return recipes

def save_recipes_to_json(path:str, recipes:Dict) -> None:
    """
    Saves a dictionary of Recipe objects to a json file
    :param path: string. The location where the json file should be created. Overwrites any existing file with the same name
    :param recipes: Dictionary containing Recipe objects
    """
    recipes_dict = {}
    for k,v in recipes.items():
        recipes_dict[k] = {}
        recipes_dict[k]["name"] = v.name
        recipes_dict[k]["ingredients"] = v.ingredients
        recipes_dict[k]["preparation"] = v.preparation
    with open(path, "w", encoding='utf-8') as f:
        json.dump(recipes_dict, f)

def add_recipe(path:str, rec:Recipe) -> None:
    """
    Adds a recipe to a json file
    :param path: string. The location of the json file
    :param rec: Recipe. The recipe to be added
    """
    json_data = load_recipes_from_json(path)
    json_data[rec.name] = rec
    save_recipes_to_json(path,json_data)


if __name__ == "__main__":
    recipes_path = "/home/jonas/Desktop/daily_gui/data/recipes.json"
    rec = Recipe("Test_recipe",["1","2","3"],"")
    add_recipe(recipes_path, rec)

