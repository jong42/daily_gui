from typing import List
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def draw_figure(canvas, figure):
    """
    helper function to integrate pyplot figures into PySimpleGUI
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def init_layout():
    """
    Initialize a layout with a blank canvas for a matplotlib plot. For adding contents to the canvas, init_gui() has
    to be called, then figures can be added with add_fig_to_gui()
    :return: layout. a PySimpleGUI layout
    """
    layout = [[sg.Canvas(key="figCanvas")]]
    return layout


def init_gui(layout):
    """
    Construct a GUI with PySimpleGUI. Figures have to be added afterwards, see add_fig_to_gui()

    layout: PySimpleGUI layout
    """
    # layout = [[sg.Text("This is a line of text")], [sg.Canvas(key='figCanvas')]]
    window = sg.Window("daily_gui", layout, resizable=True, finalize=True)
    return window


def plot_images(x, y, images, ax=None):
    """
    Creates a scatterplot with custom marker symbols from png files
    Taken from https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot
    :param x:
    :param y:
    :param images:
    :param ax:
    :return:
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


def add_figs_to_gui(
    gui,
    timestamps: List,
    temps: List,
    prec_probs: List,
    minmax_timestamps: List,
    minmax_temps: List,
    symbols: List,
):
    """
    Add pyplot figures to an existing GUI created with PySimpleGUI
    """
    # TODO: Write proper docstrings for all the functions here
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
    ax1.set_ylabel('Temperature (degrees celsius)', color="red")
    ax2.set_ylabel('Precipitation Probability', color='blue')
    # Instead of plt.show
    draw_figure(gui["figCanvas"].TKCanvas, fig)
