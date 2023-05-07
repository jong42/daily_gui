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
    _VARS = {'window': False}
    layout = [[sg.Text("This is a line of text")], [sg.Canvas(key='figCanvas')]]
    _VARS['window'] = sg.Window("daily_gui", layout, finalize=True)
    return _VARS

def add_fig_to_gui(gui, x:List, y:List):
    """
    Add a pyplot figure to an existing GUI created with PySimpleGUI
    """
    fig = plt.figure()
    plt.plot(x, y)
    # Instead of plt.show
    draw_figure(gui['window']['figCanvas'].TKCanvas, fig)