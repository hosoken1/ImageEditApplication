import sys
import os
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

#関数の定義
def ExitApplication():
    root.quit()
    sys.exit()

# rootメインウィンドウの設定
root = tk.Tk()
root.title("tkinterによるGUI画面作成")
root.geometry("300x100")

# メインフレームの作成と設置
frame = ttk.Frame(root)
frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

# 各種ウィジェットの作成
label = ttk.Label(frame, text="フォルダ指定：")
entry = ttk.Entry(frame)
button_fopen = ttk.Button(frame, text="参照")
button_execute = ttk.Button(frame, text="実行")
button_exit = ttk.Button(frame,text="終了",command = lambda:ExitApplication())

# 各種ウィジェットの設置
label.grid(row=0, column=0)
entry.grid(row=0, column=1)
button_fopen.grid(row=0, column=2)
button_execute.grid(row=1, column=1)
button_exit.grid(row=3,column=0)

root.mainloop()
