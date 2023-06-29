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
    pass


def test_save_to_json():
    pass


def test_get_index_by_name():
    pass


def test_add():
    pass


def test_delete():
    pass


def test_update():
    pass
