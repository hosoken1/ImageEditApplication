#インポート
import sys
import os
import subprocess,shlex
import tkinter as tk
from tkinter import ttk,filedialog as filedialog,messagebox
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
    ret = messagebox.askyesno('アプリケーションの終了','アプリケーションを終了しますか？')
    if(ret == True):
        root.quit()
        sys.exit()

# * ファイルの閲覧
def OpenImageOnExplorer():
    inipath = '/'
    filepath = filedialog.askopenfilename()
    entry_ImagePath.delete(0,tk.END)
    entry_ImagePath.insert(0,filepath)
    isImage = FileImageExist()
    Show_image(isImage)

#*保存先の指定
def OpenSaveFolderOnExplorer():
    inipath = '/'
    saveFolderPath = filedialog.askdirectory()
    entry_SavePath.delete(0,tk.END)
    entry_SavePath.insert(0,saveFolderPath)
#TODO: 画像の編集をする関数を作る
def EditImageMono(_img):
    _img_mono = _img.convert(mode='1')
    return _img_mono
"""
画像の保存をする関数
保存先が指定されていないまたは指定されたファイルが画像ではない場合に
保存をせずに終了する
"""
def SaveImage():
    saveFolderPath = entry_SavePath.get()
    imageFilePath = entry_ImagePath.get()
    #保存先が指定されていない、もしくは画像ファイルが指定されていないケースを検知する
    if(FileImageExist() == False or saveFolderPath == ''):
        ErrorMessage('画像ファイルが指定されていないまたは保存先を指定されていないです')
        return
    image = Image.open(imageFilePath)

    #********************画像の変換********************************
    image_mono = EditImageMono(image)
    #*************************************************************

    #*******************保存先のパスの設定*****************************************
    baseFileName = os.path.basename(imageFilePath)
    baseFileNameWithoutExt,ext = os.path.splitext(os.path.basename(baseFileName))
    print(baseFileNameWithoutExt)
    print(ext)
    savePath = saveFolderPath + '/' + baseFileName
    savePath_mono = saveFolderPath + '/' + baseFileNameWithoutExt + '_mono' + ext
    print(savePath)
    print(savePath_mono)
    #***************************************************************************
    image.save(savePath,quality=90)
    image_mono.save(savePath_mono,quality=90)


    #subprocess.Popen(["explorer",savePath],shell = True)
    #filedialog.Open(savePath)

"""
指定したファイルが画像ファイルかどうかを判定する
画像ファイルだった場合はtrueが、そうでなかった場合はfalseが返ってくる
"""
def FileImageExist():
    name, ext = os.path.splitext(entry_ImagePath.get())
    if(name == ''):
        ErrorMessage('画像ファイルを指定してください。')
        return False
    elif(ext == '.jpg' or ext == '.png'):
        return True
    else:
        ErrorMessage('これは画像ファイルではありません。')
        return False

# * エラーメッセージを表示する関数
def ErrorMessage(_message):
    text_error["text"] = _message

# * -------------画像の表示-----------------
def Show_image(_isImage):
    if(_isImage == True):
        imgPIL = Image.open(open(entry_ImagePath.get(),'rb'))
        imgPIL = imgPIL.resize((400,200))

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
text_SaveFolder = ttk.Label(frame, text='保存先：')
text_error = ttk.Label(frame, text='',foreground='#ff0000')
entry_ImagePath = ttk.Entry(frame)
entry_SavePath = ttk.Entry(frame)
button_FileOpen = ttk.Button(frame, text='参照', command=lambda:OpenImageOnExplorer())
button_SaveFolderOpen = ttk.Button(frame, text='保存先指定', command=lambda:OpenSaveFolderOnExplorer())
#TODO:画像の編集ボタンに画像の編集をする関数を割り当てる4
button_EditImage = ttk.Button(frame, text='編集設定')
button_Save = ttk.Button(frame, text='保存', command=lambda:SaveImage())
button_exit = ttk.Button(frame, text='終了', command=lambda:ExitApplication())

# * 各種ウィジェットの設置
#canvas
canvas.grid(row=0, column=1)
#raw1 SelectImageFile
text.grid(row=1, column=0)
entry_ImagePath.grid(row=1, column=1,ipadx=100)
button_FileOpen.grid(row=1, column=2)
#raw2 SelectSaveFolder
text_SaveFolder.grid(row=2, column=0)
entry_SavePath.grid(row=2, column=1,ipadx=100)
button_SaveFolderOpen.grid(row=2, column=2)
#raw3
button_Save.grid(row=3, column=2)
#raw4
button_EditImage.grid(row=4, column=2)
text_error.grid(row=4,column=1)
#raw5
button_exit.grid(row=5,column=0)

root.mainloop()
#*テスト
args = shlex.split("mkdir ./abc")
proc = subprocess.call(args)
