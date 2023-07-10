from typing import List, Dict
import json


class Recipe:
    def __init__(self, name: str, ingredients: List[str], preparation: str):
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation


class RecipeCollection:
    def __init__(self, recipes: List[Recipe] | Recipe = []):
        if isinstance(recipes, list):
            for recipe in recipes:
                if not isinstance(recipe, Recipe):
                    raise TypeError(str(recipe) + "is not of type Recipe")
            self.recipes = recipes
        elif isinstance(recipes, Recipe):
            self.recipes = [recipes]
        else:
            raise TypeError(str(recipes) + "is neither a Recipe nor a list of Recipes")

    def load_from_json(self, path: str) -> None:
        """
        Loads Recipe objects from a json file
        :param path: the location of the json file
        """
        recipes = []
        with open(path, "r", encoding="utf-8") as recipes_data:
            recipes_json = json.load(recipes_data)

            for entry in recipes_json:
                if not isinstance(entry, dict):
                    raise KeyError(str(entry) + "is not a Dictionary")
                name = recipes_json[entry]["name"]
                ingredients = recipes_json[entry]["ingredients"]
                preparation = recipes_json[entry]["preparation"]
                recipes.append(Recipe(name, ingredients, preparation))
        self.recipes = recipes

    def save_to_json(self, path: str) -> None:
        """
        Saves all recipes to a json file
        :param path: string. The location where the json file should be created. Overwrites existing files.
        """
        recipes_dict = {}
        for recipe in self.recipes:
            recipes_dict[recipe.name] = {}
            recipes_dict[recipe.name]["name"] = recipe.name
            recipes_dict[recipe.name]["ingredients"] = recipe.ingredients
            recipes_dict[recipe.name]["preparation"] = recipe.preparation
        with open(path, "w", encoding="utf-8") as f:
            json.dump(recipes_dict, f)

    def get_index_by_name(self, name: str) -> List[int]:
        """
        Find the index in the recipe list of a recipe with a given name
        :param name: string. name of the recipe
        :return: i. List of Integers. indices of the recipe in the recipes list
        """
        indices = []
        for i, recipe in enumerate(self.recipes):
            if recipe.name == name:
                indices.append(i)
        if not indices:
            raise ValueError(str(name) + "is not one of the recipe names")
        return indices

    def add(self, recipe: Recipe) -> None:
        """
        Adds a recipe to the collection
        :param recipe: Recipe. The recipe to be added
        """
        if isinstance(recipe, Recipe):
            self.recipes.append(recipe)
        else:
            raise TypeError(str(recipe) + "is not of type Recipe")

    def delete(self, name: str) -> None:
        """
        Deletes a recipe from the collection
        :param name: string. The name of the recipe to be deleted
        """
        recipes_to_delete = []
        for recipe in self.recipes:
            if recipe.name == name:
                recipes_to_delete.append(recipe)
        if not recipes_to_delete:
            raise ValueError(str(name) + "is not one of the recipe names")
        for recipe in recipes_to_delete:
            self.recipes.remove(recipe)

    def update(
        self, name: str, new_name: str = None, ing: List[str] = None, prep: str = None
    ) -> None:
        """
        Changes the contents of a recipe
        :param name: string. The existing recipe name
        :param new_name: string or None. The changed recipe name. If None, the existing name is kept
        :param ing: List of strings or None. The changed recipe ingredients. If None, the existing ingredients are kept
        :param prep: string or None. The changed recipe preparation text. If None, the existing preparation text is kept
        """
        name_exists = False
        for recipe in self.recipes:
            if recipe.name == name:
                recipe_to_update = recipe
                name_exists = True
        if not name_exists:
            raise ValueError(str(name) + "is not one of the existing recipe names")
        indices = self.get_index_by_name(name)
        for index in indices:
            if new_name:
                self.recipes[index].name = new_name
            if ing:
                self.recipes[index].ingredients = ing
            if prep:
                self.recipes[index].preparation = prep
