from typing import List
import json


class Recipe:
    def __init__(self, name: str, ingredients: List[str], preparation: str):
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation


if __name__ == "__main__":
    recipes_path = "/home/jonas/Desktop/daily_gui/data/recipes.json"
    with open(recipes_path, "r") as recipes_data:
        recipes_json = json.load(recipes_data)
    print(recipes_json)
    for entry in recipes_json:
        name = recipes_json[entry]['name']
        ingredients = recipes_json[entry]['ingredients']
        preparation = recipes_json[entry]['preparation']
        recipe = Recipe(name, ingredients, preparation)

    print(recipe.name)
    print(recipe.ingredients)
    print(recipe.preparation)
