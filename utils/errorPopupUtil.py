''' Generates standard error dialogs '''

import FreeSimpleGUI as sg
from webbrowser import open as webpage


def error(e):
    error_window = sg.Window("Error",
                             [[sg.Multiline(str(e), size=(45, 5), disabled=True)],
                              [sg.Text("Report unexpected errors on Github", enable_events=True,
                                       tooltip="Launch browser", key="link", font=("Helvetica", 9, "underline"),
                                       text_color="blue")],
                              [sg.OK(size=(41, 1))]],
                             modal=True, finalize=True, icon='PlaylistBackupIcon.ico')
    while True:
        events, values = error_window.read()
        if events == sg.WIN_CLOSED or events == "OK":
            break
        elif events == "link":
            webpage("https://github.com/SCRedstone/playlist-backup/issues", new=1)

    error_window.close()
