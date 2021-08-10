''' Options menu edits settings in config.json '''

import json
import PySimpleGUI as sg


def editor():

    # Get API keys from file
    with open("./config.json") as f:
        keys = json.load(f)
    saveLocation = keys["savePath"]

    layout = [[sg.T("Soundcloud API Key:", size=(15, 1)), sg.InputText(keys["client_id"], key="SCKey", size=(40, 1))],
              [sg.T("YouTube API Key:", size=(15, 1)), sg.InputText(keys["YT_devkey"], key="YTKey", size=(40, 1))],
              [sg.T("_"*59)],
              [sg.T("Select where to save your backups:")],
              [sg.InputText(key='directory', size=(50, 1)), sg.FolderBrowse(target='directory')],
              [sg.T("Current save location: " + saveLocation)],
              [sg.B("Save", size=(5, 1)), sg.Cancel()]]

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
            with open("./config.json", 'w', encoding='utf8') as outfile:  # Writes keys to file
                json.dump(keys, outfile, indent=2, ensure_ascii=False)
            break

    window.close()
