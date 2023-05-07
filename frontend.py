from typing import List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

def draw_figure(canvas, figure):
    """
    helper function to integrate pyplot figures into PySimpleGUI
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def init_gui():
    """
    Construct a GUI with PySimpleGUI. Figures have to be added afterwards, see add_fig_to_gui()
    """
    layout = [[sg.Text("This is a line of text")], [sg.Canvas(key='figCanvas')]]
    window = sg.Window("daily_gui", layout, finalize=True)
    return window

def add_figs_to_gui(gui, timestamps:List, temps:List, prec_probs:List):
    """
    Add pyplot figures to an existing GUI created with PySimpleGUI
    """

    fig, axs = plt.subplots(1, 2)
    axs[0].plot(timestamps, temps)
    axs[1].plot(timestamps, prec_probs)
    axs[0].set_title('Temperature')
    axs[1].set_title('Precipitation Probability')
    # Instead of plt.show
    draw_figure(gui['figCanvas'].TKCanvas, fig)