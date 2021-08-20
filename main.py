import json
import requests
from os import path
from webbrowser import open as webpage
import PySimpleGUI as sg
from utils.errorPopupUtil import error
from utils.backupCheckerUtil import backupChecker
from utils.optionsUtil import editor
from utils.playlistBackupUtil import backupMaker


def main(theme_name):
    sg.theme(theme_name)
    menu_def = [['Menu', ['Settings', 'Themes', '---', 'Exit']],
                ['Help', ['Check for Update', 'Open Github', '---', 'About']]]
    layout = [[sg.Menu(menu_def)],
              [sg.Text('Enter a playlist ID to back up:')],
              [sg.InputText(do_not_clear=False, size=(100, 1), key="ID")],
              [sg.Button('Back up!', size=(10, 1))],
              [sg.Text('_'*55)],  # Horizontal separator
              [sg.Text('Check a playlist against your backup:')],
              [sg.InputText(key='inputFile', size=(46, 1), enable_events=True), sg.FileBrowse(
                  target='inputFile', file_types=(("JSON Files", "*.json"), ("All Files", "*.*")))],
              [sg.Button('Check!', size=(10, 1))]]

    window = sg.Window('Playlist Backup Tool', layout, size=(420, 211))

    try:
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()

            # If user closes window or clicks exit
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            # When a backup file is selected, ID InputText autofills
            if event == "inputFile":
                if path.isfile(values['inputFile']):
                    try:  # See if file is JSON
                        with open(values['inputFile'], encoding='utf-8') as f:
                            playlist_data = json.load(f)
                    except:
                        continue
                    try:
                        id = playlist_data["id"]  # Soundcloud format
                    except:
                        id = playlist_data[0]["items"][0]["snippet"]["playlistId"]

                    window["inputFile"].update(values["inputFile"])  # inputFile manual fill cuz FileBrowse doesn't? idk
                    window["ID"].update(id)

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

            # Change colour schemes
            elif event == 'Themes':
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
                        with open("config.json") as f:
                            config = json.load(f)
                        config['theme'] = values['themes'][0]
                        with open("config.json", 'w', encoding='utf8') as outfile:  # Saves theme to config file
                            json.dump(config, outfile, indent=2, ensure_ascii=False)
                        theme_window.close()
                        window.close()
                        return True

            # Check for new versions of this program on Github
            elif event == "Check for Update":
                update_window = None  # update_window init
                try:
                    ver_full = requests.get("https://api.github.com/repos/SCRedstone/playlist-backup/releases/latest").json()["tag_name"]
                    ver_int = int("".join(filter(str.isdigit, ver_full)))  # Strips response to only numbers
                except Exception as e:  # Mostly for if no internet
                    error("Versioning could not be retrieved at this time.\n" + str(e))
                    continue
                if 81 < ver_int:
                    update_window = sg.Window("Updater",
                                              [[sg.T("A new update is available!", size=(25, 1))],
                                               [sg.T("Current version: v0.8.1")],
                                               [sg.T("New version: " + ver_full)],
                                               [sg.B("Open download page"), sg.B("Maybe later", key="OK")]],
                                              modal=True)
                else:
                    update_window = sg.Window("Updater",
                                              [[sg.T("There are no new updates at this time.\n")],
                                               [sg.B("OK")]],
                                              modal=True)

                while True:
                    events, values = update_window.read()
                    if events == sg.WIN_CLOSED or events == "OK":
                        break
                    elif events == "Open download page":
                        webpage("https://github.com/SCRedstone/playlist-backup/releases", new=1)
                update_window.close()

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
                    error("File not found!")
                    continue
                try:  # See if file is JSON (doesn't check if it's actually in proper format)
                    with open(values['inputFile'], encoding='utf-8') as f:
                        playlistData = json.load(f)
                except Exception as e:
                    error("Invalid JSON file.\n" + str(e))
                    continue
                backupChecker(playlistData)

        window.close()

    except Exception as e:
        error(e)

    return False


if __name__ == "__main__":
    restart = True
    while restart is True:
        try:
            with open("config.json") as file:
                config = json.load(file)
        except Exception as err:
            error(err)
            break
        restart = main(config['theme'])  # Returns True to trigger a restart
