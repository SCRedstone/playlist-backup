import json
from os import path
from webbrowser import open as webpage
import PySimpleGUI as sg
from utils.backupCheckerUtil import backupChecker
from utils.optionsUtil import editor
from utils.playlistBackupUtil import backupMaker


def main(theme_name):
    sg.theme(theme_name)
    menu_def = [['Menu', ['Settings', 'Change Theme', '---', 'Exit']],
                ['Help', ['!Check for Update', 'Open Github', '---', 'About']]]
    layout = [[sg.Menu(menu_def)],
              [sg.Text('Enter a playlist ID to back up:')],
              [sg.InputText(do_not_clear=False, size=(100, 1))],
              [sg.Button('Back up!', size=(10, 1))],
              [sg.Text('_'*55)],  # Horizontal separator
              [sg.Text('Check a playlist against your backup:')],
              [sg.InputText(key='inputFile', do_not_clear=False, size=(46, 1)), sg.FileBrowse(target='inputFile')],
              [sg.Button('Check!', size=(10, 1))]]

    window = sg.Window('Playlist Backup Tool', layout, size=(420, 211))

    try:
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()

            # If user closes window or clicks exit
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            # Opens the Github page
            elif event == 'Open Github':
                webpage("https://github.com/SCRedstone/playlist-backup", new=1)

            # Opens popup about the program
            elif event == 'About':
                about_window = sg.Window("About",
                                         [[sg.T("PLAYLIST BACKUP", font=("Helvetica", 12, "bold"))],
                                          [sg.T("v0.8.1", font=("Helvetica", 9))],
                                          [sg.T("Playlist Backup Tool is a small program to make backups of Soundcloud and YouTube playlists in order to identify any deleted or removed playlist contents.\n"
                                                "For any questions, please consult the Github repository.\n"
                                                "Made by Redstone. Thanks for your support!", size=(50, 5))],
                                          [sg.OK(size=(15, 1))]],
                                         modal=True)
                while True:
                    events, values = about_window.read()
                    if events == sg.WIN_CLOSED or events == "OK":
                        break

                about_window.close()

            # Opens settings via the menu bar
            elif event == 'Settings':
                editor()

            elif event == 'Change Theme':
                theme_window = sg.Window("Themes",
                                         [[sg.T("Current theme: " + theme_name)],
                                          [sg.Listbox(values=sg.theme_list(), key="themes", size=(21, 11))],
                                          [sg.OK()]],
                                         modal=True)
                while True:
                    events, values = theme_window.read()
                    if events == sg.WIN_CLOSED:
                        break
                    elif events == "OK":
                        theme_window.close()
                        window.close()
                        return values["themes"][0]

            # BACKUP MAKER
            elif event == "Back up!":
                if values[1] == "":  # If field is empty, nothing happens
                    continue
                backupMaker(values[1])

            # BACKUP CHECKER
            elif event == 'Check!':
                if values['inputFile'] == "":  # If field is empty, nothing happens
                    continue
                elif path.isfile(values['inputFile']) is False:  # If path is not found
                    sg.popup("File not found!")
                    continue
                try:  # See if file is JSON (doesn't check if it's actually in proper format)
                    with open(values['inputFile'], encoding='utf-8') as f:
                        playlistData = json.load(f)
                except Exception as e:
                    sg.popup("Invalid JSON file.\n", str(e), title="Error")
                    continue
                backupChecker(playlistData)

        window.close()

    except Exception as e:
        error_window = sg.Window("Error",
                            [[sg.Multiline(str(e), size=(45, 5), disabled=True)],
                             [sg.Text("Report unexpected errors on Github", enable_events=True, tooltip="Launch browser", key="link", font=("Helvetica", 9, "underline"), text_color="blue")],
                             [sg.OK(size=(41, 1))]],
                            modal=True, finalize=True)
        while True:
            events, values = error_window.read()
            if events == sg.WIN_CLOSED or events == "OK":
                break
            elif events == "link":
                webpage("https://github.com/SCRedstone/playlist-backup/issues", new=1)

        error_window.close()

    return None


if __name__ == "__main__":
    theme = 'SystemDefault'  # Default theme
    while theme is not None:
        theme = main(theme)
