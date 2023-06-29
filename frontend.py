from typing import List, Any, Dict
import numpy as np
from tkinter import Canvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import PySimpleGUI as sg
from recipes_backend import Recipe, add_recipe


def draw_figure(canvas: Canvas, figure: Figure) -> FigureCanvasTkAgg:
    """
    helper function to integrate pyplot figures into PySimpleGUI
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def init_layout() -> List[List[sg.PySimpleGUI.Canvas]]:
    """
    Initialize a layout with a blank canvas for a matplotlib plot. For adding contents to the canvas, init_gui() has
    to be called, then figures can be added with add_fig_to_gui()
    :return: layout. list of lists containing a PySimpleGUI Canvas
    """
    layout = [[sg.Canvas(key="figCanvas")]]
    return layout


def init_gui(layout: List[List[sg.PySimpleGUI.Canvas]], recipes: List) -> sg.Window:
    """
    Construct a GUI with PySimpleGUI. Figures have to be added afterwards, see add_fig_to_gui()

    :param layout: list of lists containing a PySimpleGUI Canvas. A basic blank canvas
    :returns: window. PySimpleGUI window.

    """
    recnames = [v.name for k, v in recipes.items()]

    left_col = [
        [sg.Listbox(values=recnames, size=(20, 10), key="-LIST-", enable_events=True)]
    ]
    right_col = [
        [sg.Text(key="-NAME-")],
        [sg.Text("Ingredients:")],
        [sg.Text(key="-INGREDIENTS0-")],
        [sg.Text(key="-INGREDIENTS1-")],
        [sg.Text(key="-INGREDIENTS2-")],
        [sg.Text(key="-INGREDIENTS3-")],
        [sg.Text(key="-INGREDIENTS4-")],
        [sg.Text(key="-INGREDIENTS5-")],
        [sg.Text(key="-INGREDIENTS6-")],
        [sg.Text(key="-INGREDIENTS7-")],
        [sg.Text(key="-INGREDIENTS8-")],
        [sg.Text(key="-INGREDIENTS9-")],
        [sg.Text("Preparation:")],
        [sg.Text(key="-PREPARATION-")],
    ]

    recipes_layout = [
        [sg.Column(left_col), sg.Column(right_col)],
        [sg.B("Add"), sg.B("Delete"), sg.B("Update")],
    ]

    tabgrp = [
        [
            sg.TabGroup(
                [[sg.Tab("Weather", layout)], [sg.Tab("Recipes", recipes_layout)]]
            )
        ]
    ]
    window = sg.Window("daily_gui", tabgrp, resizable=True, finalize=True)
    return window


def plot_images(x: List[Any], y: List[Any], images: List[np.ndarray], ax=None) -> None:
    """
    Creates a scatterplot with custom marker symbols from png files
    Taken from https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot
    :param x: List. The x values to be plotted
    :param y: List. The y values to be plotted
    :param images: List of numpy arrays. The images to be used as point markers
    """
    ax = ax or plt.gca()

    for xi, yi, image in zip(x, y, images):
        im = OffsetImage(image, zoom=0.1)
        im.image.axes = ax

        ab = AnnotationBbox(
            im,
            (xi, yi),
            frameon=False,
            pad=0.0,
        )

        ax.add_artist(ab)


def add_fig_to_gui(
    gui: sg.Window,
    timestamps: List[str],
    temps: List[float],
    prec_probs: List[float],
    minmax_timestamps: List[str],
    minmax_temps: List[float],
    symbols: List[np.ndarray],
) -> None:
    """
    Add  apyplot figure to an existing GUI created with PySimpleGUI
    :param gui: sg.Window
    :param timestamps: List of strings. the x-axis values for the figure
    :param temps: List of floats. The y-axis values for the figure
    :param prec_probs: List of floats. values for the second y-axis of the figure
    :param minmax_timestamps: List of strings. x-values of points that should be labeled
    :param minmax_temps: List of floats. y-values of points that should be labeled
    :param symbols: List of numpy arrays. The symbols that should replace the point markers
    """
    fig, ax1 = plt.subplots()
    ax1.plot(timestamps, temps, color="red")
    ax1.scatter(timestamps, temps)
    ax1.scatter(minmax_timestamps, minmax_temps)
    # Replace plot markers by custom symbols
    plot_images(timestamps, temps, symbols, ax=ax1)
    # Label points
    for x, y in zip(minmax_timestamps, minmax_temps):
        ax1.text(x, y, str(y)[0:4])
    # Add precipitation probabilitiy plot
    ax2 = ax1.twinx()
    ax2.plot(timestamps, prec_probs)
    # Adjust axis labels
    stepsize = 8
    xtick_positions = ax1.get_xticks()[0::stepsize]
    xtick_positions.append(ax1.get_xticks()[-1])
    xtick_labels = ax1.get_xticklabels()[0::stepsize]
    xtick_labels.append(ax1.get_xticklabels()[-1])
    label_text_org = [i.get_text() for i in xtick_labels]
    label_text_new = [i[5:-3] for i in label_text_org]
    [label.set_text(new_text) for label, new_text in zip(xtick_labels, label_text_new)]
    ax1.set_xticks(xtick_positions, xtick_labels)
    ax1.set_ylabel("Temperature (degrees celsius)", color="red")
    ax2.set_ylabel("Precipitation Probability", color="blue")
    # Instead of plt.show
    draw_figure(gui["figCanvas"].TKCanvas, fig)


def show_gui(gui: sg.Window, recipes_path: str, recipes: Dict) -> None:
    """
    displays the GUI.

    :param gui: sg.Window.
    :param recipes_path: string. the location of the recipes json file
    :param recipes: Dict. A dictionary containing Recipe objects
    :return:
    """
    while True:
        event, values = gui.read()
        if event == sg.WIN_CLOSED:
            break
        # clicking on the list in recipes tab
        elif event == "-LIST-":
            update_name = values["-LIST-"][0]
            update_ingredients = recipes[update_name].ingredients
            for i, ingredient in enumerate(update_ingredients):
                element_name = "-INGREDIENTS" + str(i) + "-"
                gui[element_name].update(ingredient)
            # current fixed number of ingredients is 10, that's were the numbers come from
            for i in range(10 - len(update_ingredients)):
                element_name = "-INGREDIENTS" + str(9 - i) + "-"
                gui[element_name].update("")
            update_preparation = recipes[update_name].preparation
            gui["-NAME-"].update(update_name)
            gui["-PREPARATION-"].update(update_preparation)
        # Button Add in Recipes tab
        elif event == "Add":
            # TODO: Refresh recipe list while window is open
            name = sg.popup_get_text("Add name")
            ingredients = sg.popup_get_text("Add ingredients")
            preparation = sg.popup_get_text("Add preparation text")
            add_recipe(recipes_path, Recipe(name, ingredients, preparation))
    gui.close()
