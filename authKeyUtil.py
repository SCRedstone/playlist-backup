import json
import PySimpleGUI as sg


def editor():

    # Get API keys from file
    with open("auth/auth-keys.json") as f:
        keys = json.load(f)

    layout = [[sg.Text("Soundcloud 'client_id' Key: "), sg.InputText(keys["client_id"], key="SCKey")],
              [sg.Text("YouTube API Key: "), sg.InputText(keys["YT_devkey"], key="YTKey")],
              [sg.B("Save"), sg.Cancel()]]

    window = sg.Window("API Keys", layout, modal=True)

    while True:
        event, values = window.read()

        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break

        elif event == 'Save':
            keys["client_id"] = values["SCKey"]
            keys["YT_devkey"] = values["YTKey"]
            try:
                with open("auth/auth-keys.json", 'w', encoding='utf8') as outfile:  # Writes keys to file
                    json.dump(keys, outfile, indent=2, ensure_ascii=False)
                sg.popup("Saved!")
            except Exception as e:
                sg.popup("Program encountered an error saving..\n", str(e), title="ERROR")
            break

    window.close()
