#インポート
import sys
import os
import tkinter as tk
from tkinter import ttk,filedialog as filedialog
from PIL import ImageTk,Image

# * rootメインウィンドウの設定など
root = tk.Tk()
root.title('tkinterによるGUI画面作成')
root.geometry('600x500')

# * メインフレームの作成と設置
frame = ttk.Frame(root)
frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

# * 関数の定義
def ExitApplication():
    root.quit()
    sys.exit()

# * ファイルの閲覧
def OpenFileOnExplorer():
    inipath = '/'
    filepath = filedialog.askopenfilename()
    entry.delete(0,tk.END)
    entry.insert(0,filepath)
    isImage = FileImageExist()
    Show_image(isImage)

# TODO: 画像の編集をする関数を作る

"""
* 指定したファイルが画像ファイルかどうかを判定する
* 画像ファイルだった場合はtrueが、そうでなかった場合はfalseが返ってくる
"""
def FileImageExist():
    name, ext = os.path.splitext(entry.get())
    #print(ext)
    if(name == ''):
        text_error["text"] = 'ファイルを指定してください。'
        return False
    elif(ext == '.jpg' or ext == '.png'):
        #text_error["text"] = 'これは画像ファイルです。'
        return True
    else:
        text_error["text"] = 'これは画像ファイルではありません。'
        return False

# * -------------画像の表示-----------------
def Show_image(_isImage):
    if(_isImage == True):
        imgPIL = Image.open(open(entry.get(),'rb'))
        imgPIL = imgPIL.resize((200,400))

        global photo_image
        photo_image = ImageTk.PhotoImage(imgPIL)

        frame.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        canvas.create_image(
            canvas_width/2,
            canvas_height/2,
            image = photo_image
        )
#*-----------------------------------------

# * 各種ウィジェットの作成
canvas = tk.Canvas(frame,bg="white", height=200, width=400)
text = ttk.Label(frame, text='フォルダ指定：')
text_error = ttk.Label(frame, text='',foreground='#ff0000')
entry = ttk.Entry(frame)
button_FileOpen = ttk.Button(frame, text='参照', command=lambda:OpenFileOnExplorer())
#TODO:画像の編集ボタンに画像の編集をする関数を割り当てる4
button_EditImage = ttk.Button(frame, text='編集')
button_execute = ttk.Button(frame, text='実行')
button_exit = ttk.Button(frame, text='終了', command=lambda:ExitApplication())

# * 各種ウィジェットの設置
canvas.grid(row=0, column=1)
text.grid(row=1, column=0)
entry.grid(row=1, column=1,ipadx=100)
button_FileOpen.grid(row=1, column=2)
button_execute.grid(row=2, column=1)
button_EditImage.grid(row=3, column=2)
text_error.grid(row=3,column=1)
button_exit.grid(row=4,column=0)

root.mainloop()
