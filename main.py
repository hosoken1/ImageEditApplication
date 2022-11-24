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
def EditImageGray(_img):
    _img_mono = _img.convert(mode='L')
    return _img_mono
def EditImageResize(_img):
    print(resize_width)
    print(resize_height)
    _img_resized = _img.resize((int(resize_width),int(resize_height)))
    return _img_resized
"""
画像の保存をする関数
*保存先が指定されていないまたは指定されたファイルが画像ではない場合に
 保存をせずに終了する。
*事前に指定された編集方法を実行する。
"""
def SaveImage():
    #各種パスの設定
    saveFolderPath = entry_SavePath.get()
    imageFilePath = entry_ImagePath.get()
    baseFileName = os.path.basename(imageFilePath)
    baseFileNameWithoutExt,ext = os.path.splitext(os.path.basename(baseFileName))
    savePath = saveFolderPath + '/' + baseFileName
    #print(baseFileNameWithoutExt)
    #print(ext)
    #print(savePath)

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
        savePath_resize = saveFolderPath + '/' + baseFileNameWithoutExt + '_resized_'+ resize_width + 'x'+ resize_height + ext        
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
"""
元の画面が動かせない状態で設定画面を開く
"""
# * --------------設定画面--------------
def CreateSettingWindow():
    settingwindow = tk.Toplevel()
    settingwindow.title('設定画面')
    settingwindow.geometry('500x300')
    settingwindow.grab_set()
    settingwindow.focus_set()
    #*各種GUIの作成
    #text
    text_deka = ttk.Label(settingwindow,text='編集の設定')
    text_save = ttk.Label(settingwindow,text='元の画像の保存')
    text_mono = ttk.Label(settingwindow,text='モノクロ画像の生成')
    text_gray = ttk.Label(settingwindow,text='グレー画像の生成')
    text_resize = ttk.Label(settingwindow,text='画像のリサイズ')
    text_resize_height = ttk.Label(settingwindow,text='Height:')
    text_resize_width = ttk.Label(settingwindow,text='Width:')
    #toggle button
    toggleB_save = ttk.Button(settingwindow, text='ON' if isSave else 'OFF',command=lambda:Switch_isSave())
    toggleB_save.bind("<ButtonPress>",Toggle_Func)
    toggleB_mono = ttk.Button(settingwindow, text='ON' if isMono else 'OFF',command=lambda:Switch_isMono())
    toggleB_mono.bind("<ButtonPress>",Toggle_Func)
    toggleB_gray = ttk.Button(settingwindow, text='ON' if isGray else 'OFF',command=lambda:Switch_isGray())
    toggleB_gray.bind("<ButtonPress>",Toggle_Func)
    toggleB_resize = ttk.Button(settingwindow, text='ON' if isResize else 'OFF',command=lambda:Switch_isResize())
    toggleB_resize.bind("<ButtonPress>",Toggle_Func)
    #Button
    button_apply = ttk.Button(settingwindow, text='適用',command=lambda:Apply())
    #Entry
    global entry_Resize_Width,entry_Resize_Height
    entry_Resize_Width = ttk.Entry(settingwindow,width=10)
    entry_Resize_Height = ttk.Entry(settingwindow,width=10)
    #*各種GUIの配置
    #1行目
    text_deka.grid(row=0,column=0)
    #2行目
    text_save.grid(row=1,column=0)
    toggleB_save.grid(row=1,column=1)
    #3行目
    text_mono.grid(row=2,column=0)
    toggleB_mono.grid(row=2,column=1)
    #4行目
    text_gray.grid(row=3,column=0)
    toggleB_gray.grid(row=3,column=1)
    #5行目
    text_resize.grid(row=4,column=0)
    toggleB_resize.grid(row=4,column=1)
    #6行目
    text_resize_width.grid(row=5,column=0)
    entry_Resize_Width.grid(row=5,column=1)
    text_resize_height.grid(row=5,column=2)
    entry_Resize_Height.grid(row=5,column=3)
    #7行目
    button_apply.grid(row=6,column=3)
    
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
# * ---------------------------------------

# * 各種ウィジェットの作成
canvas = tk.Canvas(frame,bg="white", height=200, width=400)
text = ttk.Label(frame, text='フォルダ指定：')
text_SaveFolder = ttk.Label(frame, text='保存先：')
text_error = ttk.Label(frame, text='',foreground='#ff0000')
entry_ImagePath = ttk.Entry(frame)
entry_SavePath = ttk.Entry(frame)
button_FileOpen = ttk.Button(frame, text='参照', command=lambda:OpenImageOnExplorer())
button_SaveFolderOpen = ttk.Button(frame, text='保存先指定', command=lambda:OpenSaveFolderOnExplorer())
button_EditImage = ttk.Button(frame, text='編集設定',command=lambda:CreateSettingWindow())
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