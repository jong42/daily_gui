from typing import List


class Recipe:
    def __init__(self, name: str, ingredients: List[str], preparation: str):
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation


if __name__ == "__main__":
    rec_name = "Reis mit Fisch"
    ingredients = ["Lachs", "Reis", "Öl", "saure Sahne", "Kräuter zum Würzen", "Gemüse"]
    preparation = ""
    recipe1 = Recipe(rec_name, ingredients, preparation)
