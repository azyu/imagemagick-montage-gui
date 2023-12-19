import PySimpleGUI as sg
from PIL import Image
import io
import os.path

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

sg.theme('DarkGray')

row1 = [
    [
        sg.Text("결과 파일"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.Save(),
    ],
    [
        sg.T("열"),
        sg.I(size=(4, 1), default_text="4", enable_events=True, key="-COLUMNS-"),
        sg.T("행"),
        sg.I(size=(4, 1), default_text="4", enable_events=True, key="-ROWS-"),
    ],   
    [
        sg.T("가로 px"),
        sg.I(size=(6, 1), default_text="2048", enable_events=True, key="-WIDTH-"),
        sg.T("세로 px"),
        sg.I(size=(6, 1), default_text="2048", enable_events=True, key="-HEIGHT-"),
    ],        
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],    
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("파일 추가", key="-ADDFILE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(row1),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("ImageMagick Montage GUI", layout)
file_list = []

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = values["-FILE LIST-"][0]
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(data=bio.getvalue())

        except:
            pass
    elif event == "-ADDFILE-":
        try:
            filenames = sg.popup_get_file("파일을 선택해주세요: ", multiple_files=True, file_types=file_types)
            for filename in filenames.split(';'):
                new_filename = filename.strip()
                if new_filename not in file_list:
                    file_list.append(new_filename)
                window["-FILE LIST-"].update(values=file_list)
        except:
            pass

window.close()