import sys
import os
import tkinter as tk
from tkinter import ttk as ttk
import tkinter.filedialog as filedialog

# rootメインウィンドウの設定など
#tktext = tk.StringVar()
root = tk.Tk()
root.title('tkinterによるGUI画面作成')
root.geometry('500x500')

# メインフレームの作成と設置
frame = ttk.Frame(root)
frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

#関数の定義
def ExitApplication():
    root.quit()
    sys.exit()

#ファイルの閲覧
def OpenFileOnExplorer():
    inipath = '/'
    filepath = filedialog.askopenfilename()
    entry.delete(0,tk.END)
    entry.insert(0,filepath)

#指定したファイルが画像ファイルかどうかを判定する
def FileImageExist():
    name, ext = os.path.splitext(entry.get())
    #print(ext)
    if(name == ''):
        text_error["text"] = 'ファイルを指定してください。'
        print('ファイルを指定してください。')
    elif(ext == '.jpg' or ext == '.png'):
        text_error["text"] = 'これは画像ファイルです。'
        print('これは画像ファイルです。')
    else:
        text_error["text"] = 'これは画像ファイルではありません。'
        print('これは画像ファイルではありません。')

# 各種ウィジェットの作成
text = ttk.Label(frame, text='フォルダ指定：')
text_error = ttk.Label(frame, text='',foreground='#ff0000')
entry = ttk.Entry(frame)
button_FileOpen = ttk.Button(frame, text='参照', command=lambda:OpenFileOnExplorer())
button_execute = ttk.Button(frame, text='実行', command=lambda:FileImageExist())
button_exit = ttk.Button(frame,text='終了',command = lambda:ExitApplication())

# 各種ウィジェットの設置
text.grid(row=0, column=0)
entry.grid(row=0, column=1,ipadx=40)
button_FileOpen.grid(row=0, column=2)
button_execute.grid(row=1, column=1)
text_error.grid(row=2,column=1)
button_exit.grid(row=3,column=0)

root.mainloop()
