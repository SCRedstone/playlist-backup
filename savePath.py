# Stores file save location; resets every launch for now

import PySimpleGUI as sg

SAVE_LOCATION = "backup/"


def setSave():
    try:
        global SAVE_LOCATION
        layout = [[sg.Text("Select where to save your backups")],
                  [sg.InputText(key='directory', size=(46, 1)), sg.FolderBrowse(target='directory')],
                  [sg.Text("Current save location: " + SAVE_LOCATION)],
                  [sg.B("Save"), sg.Cancel()]]

        window = sg.Window("Saves Location", layout, modal=True)

        while True:
            event, values = window.read()

            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break

            if event == "Save":
                SAVE_LOCATION = values["directory"] + "/"
                break

        window.close()

    except Exception as e:
        sg.popup(str(e), title='ERRROR!')


def getSave():
    return SAVE_LOCATION
