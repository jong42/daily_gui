import PySimpleGUI as sg

layout = [[sg.Text("This is a line of text")], [sg.Text("This is another line of text")]]
window = sg.Window("daily_gui", layout)

window.read()