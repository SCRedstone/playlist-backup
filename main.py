'''
        Custom things to do maybe:
- Display the playlist name being saved
- Select where backup files go via Options in Menu bar
- Implement checking to see if backup JSON file has proper structure to be analyzed (low priority)
- Maybe sort backupCheckerUtil output into a table instead
- Get some cool app icon
'''

import json
import os
import webbrowser
import PySimpleGUI as sg
from backupCheckerUtil import backupChecker
from playlistBackupUtil import backupMaker
from authKeyUtil import editor


def main():
    try:
        sg.theme('SystemDefault')

        menu_def = [['Menu', ['Help', 'About', '---', 'Exit']],
                    ['Settings', ['Auth Keys', '!Backup Save Path']]]
        layout = [[sg.Menu(menu_def)],
                  [sg.Text('Enter a playlist ID to back up:')],
                  [sg.InputText(do_not_clear=False, size=(100, 1))],
                  [sg.Button('Back up!')],
                  [sg.Text('_'*55)],  # Horizontal separator
                  [sg.Text('Check a playlist against your backup:')],
                  [sg.InputText(key='inputFile', do_not_clear=False, size=(46, 1)), sg.FileBrowse(target='inputFile')],
                  [sg.Button('Check!')]]

        # Create the Window
        window = sg.Window('Playlist Backup Tool', layout, size=(420, 211))

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()

            # If user closes window or clicks exit
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            # Menu 'help' opens the Github page
            elif event == 'Help':
                webbrowser.open("https://github.com/SCRedstone/playlist-backup", new=1)

            # Opens popup about the program
            elif event == 'About':
                sg.Popup("PLAYLIST BACKUP, v0.7.21\n\nA small program to make backups of Soundcloud and YouTube "
                         "playlists in order to identify deleted/removed songs.\n\nThanks for your support!\n\t"
                         "- Redstone", title="About")

            elif event == 'Auth Keys':
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
        sg.popup(str(e), title="ERROR!")


if __name__ == "__main__":
    main()
