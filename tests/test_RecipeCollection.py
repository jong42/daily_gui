import os
import json
import pytest
from daily_gui.recipes_backend import Recipe, RecipeCollection


def test_init():
    # list of Recipe objects
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe2", ["1", "2", "3"], "preparation string")
    recipe_3 = Recipe("recipe3", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3])
    assert len(rec_col.recipes) == 3
    assert rec_col.recipes[0] == recipe_1
    assert rec_col.recipes[1] == recipe_2
    assert rec_col.recipes[2] == recipe_3
    # no argument
    rec_col = RecipeCollection()
    assert rec_col.recipes == []
    # list of other objects
    with pytest.raises(TypeError):
        rec_col = RecipeCollection(["These", "are", "not", "Recipe objects"])
    # only one recipe
    rec_col = RecipeCollection(recipe_1)
    assert len(rec_col.recipes) == 1
    assert rec_col.recipes[0] == recipe_1
    # something else than a list
    with pytest.raises(TypeError):
        rec_col = RecipeCollection("This is not a list")


def test_load_from_json():
    rec_col = RecipeCollection()
    # not a string
    with pytest.raises((TypeError, OSError)):
        rec_col.load_from_json(99)
    # wrong structure of the dict in the json file
    fail_dict = {"not name": "a", "not ingredients": "b", "not prep": "c"}
    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(fail_dict, f)
    with pytest.raises(KeyError):
        rec_col.load_from_json("temp.json")
    os.remove("temp.json")


def test_save_to_json():
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe2", ["1", "2", "3"], "preparation string")
    recipe_3 = Recipe("recipe3", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3])
    # not a string
    with pytest.raises((TypeError, OSError)):
        rec_col.save_to_json(99)


def test_get_index_by_name():
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe2", ["1", "2", "3"], "preparation string")
    recipe_3 = Recipe("recipe3", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3])
    i = rec_col.get_index_by_name("recipe2")
    assert i == [1]
    # not a string
    with pytest.raises((TypeError, ValueError)):
        rec_col.get_index_by_name(99)
    # name not included in recipe names
    with pytest.raises(ValueError):
        rec_col.get_index_by_name("recipe4")
    # name more than once in recipe names
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3, recipe_3])
    i = rec_col.get_index_by_name("recipe3")
    assert i == [2, 3]


def test_add():
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe2", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1])
    rec_col.add(recipe_2)
    assert len(rec_col.recipes) == 2
    assert rec_col.recipes[1] == recipe_2
    # not a recipe
    with pytest.raises(TypeError):
        rec_col.add("This is not a recipe")


def test_delete():
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe2", ["1", "2", "3"], "preparation string")
    recipe_3 = Recipe("recipe3", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3])
    rec_col.delete("recipe3")
    assert len(rec_col.recipes) == 2
    # not a string
    with pytest.raises((TypeError, ValueError)):
        rec_col.delete(99)
    # name not in recipes
    with pytest.raises(ValueError):
        rec_col.delete("recipe4")
    # name in recipes multiple times
    rec_col = RecipeCollection([recipe_1, recipe_3, recipe_3])
    rec_col.delete("recipe3")
    assert len(rec_col.recipes) == 1


def test_update():
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1])
    rec_col.update("recipe1", "new_recipe1", ["4", "5", "6"], "new prep string")
    assert len(rec_col.recipes) == 1
    assert rec_col.recipes[0].name == "new_recipe1"
    assert rec_col.recipes[0].ingredients == ["4", "5", "6"]
    assert rec_col.recipes[0].preparation == "new prep string"
    # wrong input types
    with pytest.raises((TypeError, ValueError)):
        rec_col.update(99, "new_recipe1", ["4", "5", "6"], "new prep string")
    with pytest.raises((TypeError, ValueError)):
        rec_col.update("recipe1", 99, ["4", "5", "6"], "new prep string")
    with pytest.raises((TypeError, ValueError)):
        rec_col.update("recipe1", "new_recipe1", 99, "new prep string")
    with pytest.raises((TypeError, ValueError)):
        rec_col.update("recipe1", "new_recipe1", ["4", "5", "6"], 99)
    # name not included
    with pytest.raises(ValueError):
        rec_col.update("recipe4", "new_recipe1", ["4", "5", "6"], "new prep string")
    # name included multiple times
    recipe_1 = Recipe("recipe", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1, recipe_2])
    rec_col.update("recipe", "new_recipe", ["4", "5", "6"], "new prep string")
    assert len(rec_col.recipes) == 2
    assert rec_col.recipes[0].name == "new_recipe"
    assert rec_col.recipes[0].ingredients == ["4", "5", "6"]
    assert rec_col.recipes[0].preparation == "new prep string"
    assert rec_col.recipes[1].name == "new_recipe"
    assert rec_col.recipes[1].ingredients == ["4", "5", "6"]
    assert rec_col.recipes[1].preparation == "new prep string"
