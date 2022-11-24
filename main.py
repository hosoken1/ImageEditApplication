#インポート
import sys
import os
import tkinter as tk
from tkinter import ttk,filedialog as filedialog,messagebox
from PIL import ImageTk,Image

#初期化
isSave = True
isMono = True
isGray = True
isResize = True
resize_width = 0
resize_height = 0

# * rootメインウィンドウの設定など
root = tk.Tk()
root.title('tkinterによるGUI画面作成')
root.geometry('600x400')


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

# * 文字列検証関数
def Validation(before_word, after_word):
    return ((after_word.isdecimal()) and (len(after_word)<=4)) or (len(after_word) == 0)

#*-------------画像の編集をする関数----------------------------------------
def EditImageMono(_img):
    _img_mono = _img.convert(mode='1')
    return _img_mono

def EditImageGray(_img):
    _img_mono = _img.convert(mode='L')
    return _img_mono

def EditImageResize(_img):
    print(resize_width)
    print(resize_height)
    _img_resized = _img.resize((int(resize_width),int(resize_height)))
    return _img_resized
#*-----------------------------------------------------------------------
"""
画像の保存をする関数
保存先が指定されていないまたは指定されたファイルが画像ではない場合に
保存をせずに終了する。
事前に指定された編集方法を実行する。
"""
def SaveImage():
    #各種パスの設定
    saveFolderPath = entry_SavePath.get()
    imageFilePath = entry_ImagePath.get()
    baseFileName = os.path.basename(imageFilePath)
    baseFileNameWithoutExt,ext = os.path.splitext(os.path.basename(baseFileName))
    savePath = saveFolderPath + '/' + baseFileName

    #保存先が指定されていない、もしくは画像ファイルが指定されていないケースを検知する
    if(FileImageExist() == False or saveFolderPath == ''):
        ErrorMessage('画像ファイルが指定されていないまたは保存先を指定されていないです')
        return
    #元の画像の読み込み
    image = Image.open(imageFilePath)

    #元の画像を保存する
    if(isSave == True):
        image.save(savePath,quality=90)

    #***************モノクロ画像への変換******************************
    if(isMono==True):
        image_mono = EditImageMono(image)
        savePath_mono = saveFolderPath + '/' + baseFileNameWithoutExt + '_mono' + ext
        image_mono.save(savePath_mono,quality=90)
        print(savePath_mono)
    #***************グレー画像への変換*******************************
    if(isGray==True):
        image_gray = EditImageGray(image)
        savePath_gray = saveFolderPath + '/' + baseFileNameWithoutExt + '_gray' + ext
        image_gray.save(savePath_gray,quality=90)
        print(savePath_gray)
    if(isResize == True):
        image_resized = EditImageResize(image)
        savePath_resize = saveFolderPath + '/' + baseFileNameWithoutExt + '_resized_'+ resize_width + 'x'+ resize_height + ext  # type: ignore
        image_resized.save(savePath_resize,quality=90)
        print(savePath_resize)
    #***************************************************************************

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
    text_Error["text"] = _message

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
"""
元の画面が動かせない状態で設定画面を開く
"""
# * --------------設定画面--------------------------------------------
def CreateSettingWindow():
    settingWindow = tk.Toplevel()
    settingWindow.title('設定画面')
    settingWindow.geometry('500x300')
    settingWindow.grab_set()
    settingWindow.focus_set()

    #*各種GUIの作成
    #text
    text_Title = ttk.Label(settingWindow,text='編集の設定')
    text_Save = ttk.Label(settingWindow,text='元の画像の保存')
    text_Mono = ttk.Label(settingWindow,text='モノクロ画像の生成')
    text_Gray = ttk.Label(settingWindow,text='グレー画像の生成')
    text_Resize = ttk.Label(settingWindow,text='画像のリサイズ')
    text_Resize_Height = ttk.Label(settingWindow,text='Height:')
    text_Resize_Width = ttk.Label(settingWindow,text='Width:')
    #toggle button
    toggleB_Save = ttk.Button(settingWindow, text='ON' if isSave else 'OFF',command=lambda:Switch_isSave())
    toggleB_Save.bind("<ButtonPress>",Toggle_Func)
    toggleB_Mono = ttk.Button(settingWindow, text='ON' if isMono else 'OFF',command=lambda:Switch_isMono())
    toggleB_Mono.bind("<ButtonPress>",Toggle_Func)
    toggleB_Gray = ttk.Button(settingWindow, text='ON' if isGray else 'OFF',command=lambda:Switch_isGray())
    toggleB_Gray.bind("<ButtonPress>",Toggle_Func)
    toggleB_Resize = ttk.Button(settingWindow, text='ON' if isResize else 'OFF',command=lambda:Switch_isResize())
    toggleB_Resize.bind("<ButtonPress>",Toggle_Func)
    #Button
    button_Apply = ttk.Button(settingWindow, text='適用',command=lambda:Apply())
    #Entry
    global entry_Resize_Width,entry_Resize_Height
    entry_Resize_Width = ttk.Entry(settingWindow,width=10)
    entry_Resize_Width.insert(0,str(resize_width))
    entry_Resize_Height = ttk.Entry(settingWindow,width=10)
    entry_Resize_Height.insert(0,str(resize_height))

    #Validate機能を使って文字制限をかけたいが動かない
    vcmd_Resize_Height = (entry_Resize_Height.register(Validation), '%s', '%P')
    vcmd_Resize_Width = (entry_Resize_Width.register(Validation), '%s', '%P')
    entry_Resize_Height.configure(validate='key', validatecommand=vcmd_Resize_Height)
    entry_Resize_Width.configure(validate='key', validatecommand=vcmd_Resize_Width)

    #*-----------------各種GUIの配置-------------------
    #---------------------1行目-----------------------
    text_Title.grid(row=0,column=0)
    #---------------------2行目-----------------------
    text_Save.grid(row=1,column=0)
    toggleB_Save.grid(row=1,column=1)
    #---------------------3行目-----------------------
    text_Mono.grid(row=2,column=0)
    toggleB_Mono.grid(row=2,column=1)
    #---------------------4行目-----------------------
    text_Gray.grid(row=3,column=0)
    toggleB_Gray.grid(row=3,column=1)
    #---------------------5行目-----------------------
    text_Resize.grid(row=4,column=0)
    toggleB_Resize.grid(row=4,column=1)
    #---------------------6行目-----------------------
    text_Resize_Width.grid(row=5,column=0)
    entry_Resize_Width.grid(row=5,column=1)
    text_Resize_Height.grid(row=5,column=2)
    entry_Resize_Height.grid(row=5,column=3)
    button_Apply.grid(row=5,column=4)
    #---------------------7行目-----------------------
    #*------------------------------------------------
def Toggle_Func(event):
    if(event.widget.cget("text") == 'ON'):
        event.widget["text"] = 'OFF'
    elif(event.widget.cget("text") == 'OFF'):
        event.widget["text"] = 'ON'
def Switch_isSave():
    global isSave
    isSave = not isSave
def Switch_isMono():
    global isMono
    isMono = not isMono
def Switch_isGray():
    global isGray
    isGray = not isGray
def Switch_isResize():
    global isResize
    isResize = not isResize
def Apply():
    global resize_width,resize_height
    resize_width = entry_Resize_Width.get()
    resize_height = entry_Resize_Height.get()

# * -----------------------------------------------------------------

# * --------------各種ウィジェットの作成-------------------------------
canvas = tk.Canvas(frame,bg="white", height=200, width=400)
text = ttk.Label(frame, text='フォルダ指定：')
text_SaveFolder = ttk.Label(frame, text='保存先：')
text_Error = ttk.Label(frame, text='',foreground='#ff0000')
entry_ImagePath = ttk.Entry(frame)
entry_SavePath = ttk.Entry(frame)
button_FileOpen = ttk.Button(frame, text='参照', command=lambda:OpenImageOnExplorer())
button_SaveFolderOpen = ttk.Button(frame, text='保存先指定', command=lambda:OpenSaveFolderOnExplorer())
button_EditImage = ttk.Button(frame, text='編集設定',command=lambda:CreateSettingWindow())
button_Save = ttk.Button(frame, text='保存', command=lambda:SaveImage())
button_exit = ttk.Button(frame, text='終了', command=lambda:ExitApplication())
#*--------------------------------------------------------------------
# * -----------------各種ウィジェットの設置-----------------------------
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
#raw3 SaveButton
button_Save.grid(row=3, column=2)
#raw4 EditSettingWindow & announce
button_EditImage.grid(row=4, column=2)
text_Error.grid(row=4,column=1)
#raw5 ExitApplication
button_exit.grid(row=5,column=0)
#*----------------------------------------------------------------
root.mainloop()