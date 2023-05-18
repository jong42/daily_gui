from typing import List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg


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
    window = sg.Window("daily_gui", layout, finalize=True)
    return window


def add_figs_to_gui(
    gui,
    timestamps: List,
    temps: List,
    prec_probs: List,
    minmax_timestamps: List,
    minmax_temps: List,
):
    """
    Add pyplot figures to an existing GUI created with PySimpleGUI
    """
    # TODO Combine temp and prec_prob into one plot with different axis
    # TODO: Write proper docstrings for all the functions here
    fig, axs = plt.subplots(1, 2, figsize=(16, 9))
    axs[0].plot(timestamps, temps, color="red")
    axs[0].scatter(timestamps, temps)
    axs[0].scatter(minmax_timestamps, minmax_temps)
    # Label points
    for x, y in zip(minmax_timestamps, minmax_temps):
        axs[0].text(x, y, str(y)[0:4])
    axs[1].plot(timestamps, prec_probs)
    axs[0].set_title("Temperature")
    axs[1].set_title("Precipitation Probability")
    # Adjust axis labels
    stepsize = 8
    xtick_positions = axs[0].get_xticks()[0::stepsize]
    xtick_positions.append(axs[0].get_xticks()[-1])
    xtick_labels = axs[0].get_xticklabels()[0::stepsize]
    xtick_labels.append(axs[0].get_xticklabels()[-1])
    label_text_org = [i.get_text() for i in xtick_labels]
    label_text_new = [i[5:-3] for i in label_text_org]
    [label.set_text(new_text) for label, new_text in zip(xtick_labels, label_text_new)]
    axs[0].set_xticks(xtick_positions, xtick_labels)
    xtick_positions = axs[1].get_xticks()[0::stepsize]
    xtick_positions.append(axs[1].get_xticks()[-1])
    xtick_labels = axs[1].get_xticklabels()[0::stepsize]
    xtick_labels.append(axs[1].get_xticklabels()[-1])
    label_text_org = [i.get_text() for i in xtick_labels]
    label_text_new = [i[5:-3] for i in label_text_org]
    [label.set_text(new_text) for label, new_text in zip(xtick_labels, label_text_new)]
    axs[1].set_xticks(xtick_positions, xtick_labels)
    # Instead of plt.show
    draw_figure(gui["figCanvas"].TKCanvas, fig)
