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
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
        rec_col.save_to_json(99)


def test_get_index_by_name():
    recipe_1 = Recipe("recipe1", ["1", "2", "3"], "preparation string")
    recipe_2 = Recipe("recipe2", ["1", "2", "3"], "preparation string")
    recipe_3 = Recipe("recipe3", ["1", "2", "3"], "preparation string")
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3])
    i = rec_col.get_index_by_name("recipe2")
    assert i == 1
    # not a string
    with pytest.raises(TypeError):
        rec_col.get_index_by_name(99)
    # name not included in recipe names
    with pytest.raises(ValueError):
        rec_col.get_index_by_name("recipe4")
    # name more than once in recipe names
    rec_col = RecipeCollection([recipe_1, recipe_2, recipe_3, recipe_3])
    i = rec_col.get_index_by_name("recipe3")
    assert i == 2  # Get index of first occurence in this case


def test_add():
    pass


def test_delete():
    pass


def test_update():
    pass
