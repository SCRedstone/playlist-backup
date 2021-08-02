import json
import os
import PySimpleGUI as sg
from utils.backupCheckerUtil import backupChecker
from utils.playlistBackupUtil import backupMaker
from utils.optionsUtil import editor
from webbrowser import open as webpage


def main():
    sg.theme('SystemDefault')

    menu_def = [['Menu', ['Settings', '---', 'Exit']],
                ['Help', ['Github', 'About']]]
    layout = [[sg.Menu(menu_def)],
              [sg.Text('Enter a playlist ID to back up:')],
              [sg.InputText(do_not_clear=False, size=(100, 1))],
              [sg.Button('Back up!')],
              [sg.Text('_'*55)],  # Horizontal separator
              [sg.Text('Check a playlist against your backup:')],
              [sg.InputText(key='inputFile', do_not_clear=False, size=(46, 1)), sg.FileBrowse(target='inputFile')],
              [sg.Button('Check!')]]

    window = sg.Window('Playlist Backup Tool', layout, size=(420, 211))

    try:
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()

            # If user closes window or clicks exit
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            # Opens the Github page
            elif event == 'Github':
                webpage("https://github.com/SCRedstone/playlist-backup", new=1)

            # Opens popup about the program
            elif event == 'About':
                sg.Popup("PLAYLIST BACKUP, v0.8.1\n\nA small program to make backups of Soundcloud and YouTube "
                         "playlists in order to identify deleted/removed songs.\n\nThanks for your support!\n\t"
                         "- Redstone", title="About")

            # Opens settings via the menu bar
            elif event == 'Settings':
                editor()

            # BACKUP MAKER
            elif event == "Back up!":
                if values[1] == "":  # If field is empty, nothing happens
                    continue
                backupMaker(values[1])

            # BACKUP CHECKER
            elif event == 'Check!':
                if values['inputFile'] == "":  # If field is empty, nothing happens
                    continue
                elif os.path.isfile(values['inputFile']) is False:  # If path is not found
                    sg.popup("File not found!")
                    continue
                try:  # See if file is JSON (doesn't check if it's actually in proper format)
                    with open(values['inputFile'], encoding='utf-8') as f:
                        playlistData = json.load(f)
                except Exception as e:
                    sg.popup("Invalid JSON file.\n", str(e))
                    continue
                backupChecker(playlistData)

        window.close()

    except Exception as e:
        window2 = sg.Window("Error",
                            [[sg.Multiline(str(e), size=(45, 5), disabled=True)],
                             [sg.Text("Report unexpected errors on Github", enable_events=True, tooltip="Launch browser", key="link", font=("Helvetica", 9, "underline"), text_color="blue")],
                             [sg.OK(size=(41, 1))]],
                            modal=True, finalize=True)
        while True:
            events, values = window2.read()
            if events == sg.WIN_CLOSED or events == "OK":
                break
            elif events == "link":
                webpage("https://github.com/SCRedstone/playlist-backup/issues", new=1)


if __name__ == "__main__":
    main()
