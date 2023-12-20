import subprocess
import PySimpleGUI as sg
from PIL import Image
import io
import os.path

file_types = [("JPEG (*.jpg)", "*.jpg"), ("PNG (*.png)", "*.png"), ("All files (*.*)", "*.*")]

sg.theme('DarkGray')

row1 = [
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
    [
        sg.Button("저장하기", key="-DO-PROCESS-")
    ]
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        ),
        sg.Button("↑", key="-UP-SELECTED-FILE-"),
        sg.Button("↓", key="-DOWN-SELECTED-FILE-"),
    ],    
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [
        sg.Button("사진 파일 추가", key="-ADD-FILE-LIST-"),
        sg.Button("사진 파일 제거", key="-REMOVE-FILE-LIST-"),
        sg.Button("모든 사진 파일 제거", key="-CLEAR-FILE-LIST-")
    ]    
]

# ----- Full layout -----
layout = [
    [
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(row1)
    ]
]

window = sg.Window("ImageMagick Montage GUI (a.k.a. 연말결산 제작기) 0.0.1", layout)
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
    elif event == "-UP-SELECTED-FILE-":
        try:
            filename = values["-FILE LIST-"][0]
            if os.path.exists(filename):
                index = file_list.index(filename)
                if index > 0:
                    file_list[index - 1], file_list[index] = file_list[index], file_list[index - 1]
                window["-FILE LIST-"].update(values=file_list)                    
        except:
            pass

    elif event == "-DOWN-SELECTED-FILE-":
        try:
            filename = values["-FILE LIST-"][0]
            if os.path.exists(filename):
                index = file_list.index(filename)
                if index < len(file_list) - 1:
                    file_list[index + 1], file_list[index] = file_list[index], file_list[index + 1]
                window["-FILE LIST-"].update(values=file_list)                    
        except:
            pass

    elif event == "-ADD-FILE-LIST-":
        try:
            filenames = sg.popup_get_file("파일을 선택해주세요: ", multiple_files=True, file_types=file_types)
            for filename in filenames.split(';'):
                new_filename = filename.strip()
                if new_filename not in file_list:
                    file_list.append(new_filename)
                window["-FILE LIST-"].update(values=file_list)
        except:
            pass

    elif event == "-REMOVE-FILE-LIST-":
        try:
            filename = values["-FILE LIST-"][0]
            if os.path.exists(filename):
                file_list.remove(filename)
                window["-FILE LIST-"].update(values=file_list)
                window["-TOUT-"].update('')
                window["-IMAGE-"].update(data='')
        except:
            pass

    elif event == "-CLEAR-FILE-LIST-":
        try:
            file_list.clear()
            window["-FILE LIST-"].update(values=file_list)
            window["-TOUT-"].update('')
            window["-IMAGE-"].update(data='')            
        except:
            pass

    elif event == "-DO-PROCESS-":
        try:
            columns = int(values["-COLUMNS-"])
            rows = int(values["-ROWS-"])
            width = int(values["-WIDTH-"])
            height = int(values["-HEIGHT-"])
            geometry_x = int(width / columns)
            geometry_y = int(height / rows)

            if columns < 1 or rows < 1 or width < 1 or height < 1:
                sg.popup("열, 행, 가로, 세로는 1 이상의 정수여야 합니다.")
                continue

            if len(file_list) < columns * rows:
                sg.popup("열, 행보다 파일의 개수가 적습니다.")
                continue

            filename = sg.popup_get_file("저장하실 파일을 지정해주세요: ", file_types=file_types, save_as=True)

            if filename is None:
                continue

            for i in range(len(file_list)):
                file_list[i] = '"' + file_list[i] + '"'

            cmd = "magick montage -auto-orient -tile {}x{} -geometry {}x{}+0+0 {} - | magick convert -gravity center -extent {}x{} - {}".format(columns, rows, geometry_x, geometry_y, " ".join(file_list), width, height, filename)
            subprocess.Popen(cmd, shell=True)
            
            sg.popup("저장했습니다.")

        except Exception as e:
            sg.popup("에러가 발생했습니다.", e)
            pass

window.close()