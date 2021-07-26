''' Options menu edits the program options via config.json '''

import json
import PySimpleGUI as sg


def editor():

    # Get API keys from file
    with open("./config.json") as f:
        keys = json.load(f)
    saveLocation = keys["savePath"]

    layout = [[sg.Text("Soundcloud API Key:"), sg.InputText(keys["client_id"], key="SCKey", size=(39, 1))],
              [sg.Text("YouTube API Key:"), sg.InputText(keys["YT_devkey"], key="YTKey", size=(41, 1))],
              [sg.Text("_"*58)],
              [sg.Text("Select where to save your backups:")],
              [sg.InputText(key='directory', size=(50, 1)), sg.FolderBrowse(target='directory')],
              [sg.Text("Current save location: " + saveLocation)],
              [sg.B("Save"), sg.Cancel()]]

    window = sg.Window("Options", layout, modal=True)

    while True:
        event, values = window.read()

        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break

        elif event == 'Save':
            keys["client_id"] = values["SCKey"]
            keys["YT_devkey"] = values["YTKey"]
            if values["directory"] != "":  # If the field is empty, it won't save a blank
                keys["savePath"] = values["directory"] + "/"

            try:
                with open("./config.json", 'w', encoding='utf8') as outfile:  # Writes keys to file
                    json.dump(keys, outfile, indent=2, ensure_ascii=False)
            except Exception as e:
                sg.popup("Program encountered an error saving..\n", str(e), title="ERROR")
            break

    window.close()
