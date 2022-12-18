#インポート
import sys
import os
import json
import tkinter as tk
from tkinter import ttk,filedialog as filedialog,messagebox
from PIL import ImageTk,Image

class Application(tk.Frame):
    def __init__(self):
        #初期化
        settingData = self.LoadData()
        self.isSave = settingData['isSave']
        self.isMono = settingData['isMono']
        self.isGray = settingData['isGray']
        self.isResize = settingData['isResize']
        self.isCrop = settingData['isCrop']
        self.resize_width = settingData['resize_width']
        self.resize_height = settingData['resize_height']
        self.crop_Left = settingData['crop_Left']
        self.crop_Right = settingData['crop_Right']
        self.crop_Up = settingData['crop_Up']
        self.crop_Down = settingData['crop_Down']

        # * rootメインウィンドウの設定など
        self.root = tk.Tk()
        self.root.title('tkinterによるGUI画面作成')
        self.root.geometry('600x400')


        # * メインフレームの作成と設置
        self.frame = ttk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)
        self.create_main()

    def main(self):
        self.root.mainloop()

    # * 関数の定義
    def ExitApplication(self):
        ret = messagebox.askyesno('アプリケーションの終了','アプリケーションを終了しますか？')
        if(ret == True):
            self.root.quit()
            sys.exit()

    #--------JSONを扱う関数の定義-------------------------
    def LoadData(self):
        rpath = r'./savedata.json'
        with open(rpath,"r") as saveData:
            data_dict = json.load(saveData)
            data_json = json.dumps(data_dict)
            print('{}'.format(data_json))
        return data_dict
    def SaveData(self):
        rpath = r'./savedata.json'
        tempData = self.LoadData()
        tempData['isSave'] = self.isSave
        tempData['isMono'] = self.isMono
        tempData['isGray'] = self.isGray
        tempData['isResize'] = self.isResize
        tempData['isCrop'] = self.isCrop
        tempData['resize_width'] = self.resize_width
        tempData['resize_height'] = self.resize_height
        tempData['crop_Left'] = self.crop_Left
        tempData['crop_Right'] = self.crop_Right
        tempData['crop_Up'] = self.crop_Up
        tempData['crop_Down'] = self.crop_Down

        with open(rpath,mode='w') as saveF:
            saveF.seek(0)
            json.dump(tempData,saveF,indent=4)
            saveF.truncate()
    #--------------------------------------------------

    # * ファイルの閲覧
    def OpenImageOnExplorer(self):
        inipath = '/'
        filepath = filedialog.askopenfilename()
        self.entry_ImagePath.delete(0,tk.END)
        self.entry_ImagePath.insert(0,filepath)
        isImage = self.FileImageExist()
        self.Show_image(isImage)

    #*保存先の指定
    def OpenSaveFolderOnExplorer(self):
        inipath = '/'
        saveFolderPath = filedialog.askdirectory()
        self.entry_SavePath.delete(0,tk.END)
        self.entry_SavePath.insert(0,saveFolderPath)

    # * 文字列検証関数
    def Validation(self,before_word, after_word):
        return ((after_word.isdecimal()) and (len(after_word)<=4)) or (len(after_word) == 0)

    #*-------------画像の編集をする関数----------------------------------------
    def EditImageMono(self,_img):
        _img_mono = _img.convert(mode='1')
        return _img_mono
    def EditImageGray(self,_img):
        _img_mono = _img.convert(mode='L')
        return _img_mono
    def EditImageResize(self,_img):
        print(self.resize_width)
        print(self.resize_height)
        _img_resized = _img.resize((int(self.resize_width),int(self.resize_height)))
        return _img_resized
    def EditImageCrop(self,_img):
        print(self.crop_Left)
        print(self.crop_Right)
        print(self.crop_Up)
        print(self.crop_Down)
        _img_croped = _img.crop((int(self.crop_Left),int(self.crop_Up),int(self.crop_Right),int(self.crop_Down)))
        return _img_croped
    #*-----------------------------------------------------------------------
    """
    画像の保存をする関数
    保存先が指定されていないまたは指定されたファイルが画像ではない場合に
    保存をせずに終了する。
    事前に指定された編集方法を実行する。
    """
    def SaveImage(self):
        #各種パスの設定
        saveFolderPath = self.entry_SavePath.get()
        imageFilePath = self.entry_ImagePath.get()
        baseFileName = os.path.basename(imageFilePath)
        baseFileNameWithoutExt,ext = os.path.splitext(os.path.basename(baseFileName))
        savePath = saveFolderPath + '/' + baseFileName

        #保存先が指定されていない、もしくは画像ファイルが指定されていないケースを検知する
        if(self.FileImageExist() == False or saveFolderPath == ''):
            self.ErrorMessage('画像ファイルが指定されていないまたは保存先を指定されていないです')
            return
        else:
            self.ErrorMessage('')
        #元の画像の読み込み
        image = Image.open(imageFilePath)

        #元の画像を保存する
        if(self.isSave == True):
            image.save(savePath,quality=90)

        #***************モノクロ画像への変換******************************
        if(self.isMono==True):
            image_mono = self.EditImageMono(image)
            savePath_mono = saveFolderPath + '/' + baseFileNameWithoutExt + '_mono' + ext
            image_mono.save(savePath_mono,quality=90)
            print(savePath_mono)
        #***************グレー画像への変換*******************************
        if(self.isGray==True):
            image_gray = self.EditImageGray(image)
            savePath_gray = saveFolderPath + '/' + baseFileNameWithoutExt + '_gray' + ext
            image_gray.save(savePath_gray,quality=90)
            print(savePath_gray)
        #***************画像のリサイズ**********************************
        if(self.isResize == True):
            image_resized = self.EditImageResize(image)
            savePath_resize = saveFolderPath + '/' + baseFileNameWithoutExt + '_resized_'+ self.resize_width + 'x'+ self.resize_height + ext
            image_resized.save(savePath_resize,quality=90)
            print(savePath_resize)
        #***************画像の切り抜き**********************************
        if(self.isCrop == True):
            image_Croped = self.EditImageCrop(image)
            savePath_Crop = saveFolderPath + '/' + baseFileNameWithoutExt + '_crop'+ ext
            image_Croped.save(savePath_Crop,quality=90)
            print(savePath_Crop)
        #***************************************************************************

    """
    指定したファイルが画像ファイルかどうかを判定する
    画像ファイルだった場合はtrueが、そうでなかった場合はfalseが返ってくる
    """
    def FileImageExist(self):
        name, ext = os.path.splitext(self.entry_ImagePath.get())
        if(name == ''):
            self.ErrorMessage('画像ファイルを指定してください。')
            return False
        elif(ext == '.jpg' or ext == '.png'):
            self.ErrorMessage('')
            return True
        else:
            self.ErrorMessage('これは画像ファイルではありません。')
            return False

    # * エラーメッセージを表示する関数
    def ErrorMessage(self,_message):
        self.text_Error["text"] = _message

    # * -------------画像の表示-----------------
    def Show_image(self,_isImage):
        if(_isImage == True):
            imgPIL = Image.open(open(self.entry_ImagePath.get(),'rb'))
            imgPIL = imgPIL.resize((400,200))

            global photo_image
            photo_image = ImageTk.PhotoImage(imgPIL)

            self.frame.update()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.canvas.create_image(
                canvas_width/2,
                canvas_height/2,
                image = photo_image
            )
    #*-----------------------------------------
    """
    元の画面が動かせない状態で設定画面を開く
    """
    # * --------------設定画面--------------------------------------------
    def CreateSettingWindow(self):
        global settingWindow
        self.settingWindow = tk.Toplevel()
        self.settingWindow.title('設定画面')
        self.settingWindow.geometry('500x300')
        self.settingWindow.grab_set()
        self.settingWindow.focus_set()

        #*各種GUIの作成
        #text
        text_Title = ttk.Label(self.settingWindow,text='編集の設定')
        text_Save = ttk.Label(self.settingWindow,text='元の画像の保存')
        text_Mono = ttk.Label(self.settingWindow,text='モノクロ画像の生成')
        text_Gray = ttk.Label(self.settingWindow,text='グレー画像の生成')
        text_Resize = ttk.Label(self.settingWindow,text='画像のリサイズ')
        text_Resize_Height = ttk.Label(self.settingWindow,text='Height:')
        text_Resize_Width = ttk.Label(self.settingWindow,text='Width:')
        text_Crop = ttk.Label(self.settingWindow,text='画像の切り抜き')
        text_Crop_Left = ttk.Label(self.settingWindow,text='左：')
        text_Crop_Right = ttk.Label(self.settingWindow,text='右:')
        text_Crop_Up = ttk.Label(self.settingWindow,text='上：')
        text_Crop_Down = ttk.Label(self.settingWindow,text='下:')
        #toggle button
        toggleB_Save = ttk.Button(self.settingWindow, text='ON' if self.isSave else 'OFF',command=lambda:self.Switch_isSave())
        toggleB_Save.bind("<ButtonPress>",self.Toggle_Func)
        toggleB_Mono = ttk.Button(self.settingWindow, text='ON' if self.isMono else 'OFF',command=lambda:self.Switch_isMono())
        toggleB_Mono.bind("<ButtonPress>",self.Toggle_Func)
        toggleB_Gray = ttk.Button(self.settingWindow, text='ON' if self.isGray else 'OFF',command=lambda:self.Switch_isGray())
        toggleB_Gray.bind("<ButtonPress>",self.Toggle_Func)
        toggleB_Resize = ttk.Button(self.settingWindow, text='ON' if self.isResize else 'OFF',command=lambda:self.Switch_isResize())
        toggleB_Resize.bind("<ButtonPress>",self.Toggle_Func)
        toggleB_Crop = ttk.Button(self.settingWindow, text='ON' if self.isCrop else 'OFF',command=lambda:self.Switch_isCrop())
        toggleB_Crop.bind("<ButtonPress>",self.Toggle_Func)
        #Button
        button_Apply_Resize = ttk.Button(self.settingWindow, text='適用',command=lambda:self.Apply_Resize())
        button_Apply_Crop = ttk.Button(self.settingWindow, text='適用',command=lambda:self.Apply_Crop())
        button_Quit_Setting = ttk.Button(self.settingWindow,text='設定を保存',command=lambda:self.Quit_Setting())
        #Entry-Resize
        global entry_Resize_Width,entry_Resize_Height
        self.entry_Resize_Width = ttk.Entry(self.settingWindow,width=10)
        self.entry_Resize_Width.insert(0,str(self.resize_width))
        self.entry_Resize_Height = ttk.Entry(self.settingWindow,width=10)
        self.entry_Resize_Height.insert(0,str(self.resize_height))
        #Entry-Crop
        global entry_Crop_Left,entry_Crop_Right,entry_Crop_Up,entry_Crop_Down
        self.entry_Crop_Left = ttk.Entry(self.settingWindow,width=8)
        self.entry_Crop_Left.insert(0,str(self.crop_Left))
        self.entry_Crop_Right = ttk.Entry(self.settingWindow,width=8)
        self.entry_Crop_Right.insert(0,str(self.crop_Right))
        self.entry_Crop_Up = ttk.Entry(self.settingWindow,width=8)
        self.entry_Crop_Up.insert(0,str(self.crop_Up))
        self.entry_Crop_Down = ttk.Entry(self.settingWindow,width=8)
        self.entry_Crop_Down.insert(0,str(self.crop_Down))
        #-------------------Validate機能を使って文字制限をかける-------------------------------
        #entry-Resize
        vcmd_Resize_Height = (self.entry_Resize_Height.register(self.Validation), '%s', '%P')
        vcmd_Resize_Width = (self.entry_Resize_Width.register(self.Validation), '%s', '%P')
        self.entry_Resize_Height.configure(validate='key', validatecommand=vcmd_Resize_Height)
        self.entry_Resize_Width.configure(validate='key', validatecommand=vcmd_Resize_Width)
        #entry-Crop
        vcmd_Crop_Left = (self.entry_Crop_Left.register(self.Validation), '%s', '%P')
        vcmd_Crop_Right = (self.entry_Crop_Right.register(self.Validation), '%s', '%P')
        vcmd_Crop_Up = (self.entry_Crop_Up.register(self.Validation), '%s', '%P')
        vcmd_Crop_Down = (self.entry_Crop_Down.register(self.Validation), '%s', '%P')
        self.entry_Crop_Left.configure(validate='key', validatecommand=vcmd_Crop_Left)
        self.entry_Crop_Right.configure(validate='key', validatecommand=vcmd_Crop_Right)
        self.entry_Crop_Up.configure(validate='key', validatecommand=vcmd_Crop_Up)
        self.entry_Crop_Down.configure(validate='key', validatecommand=vcmd_Crop_Down)
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
        self.entry_Resize_Width.grid(row=5,column=1)
        text_Resize_Height.grid(row=5,column=2)
        self.entry_Resize_Height.grid(row=5,column=3)
        button_Apply_Resize.grid(row=5,column=4)
        #---------------------7行目-----------------------
        text_Crop.grid(row=6,column=0)
        toggleB_Crop.grid(row=6,column=1)
        #---------------------8行目-----------------------
        text_Crop_Left.grid(row=7,column=0)
        self.entry_Crop_Left.grid(row=7,column=1)
        text_Crop_Right.grid(row=7,column=2)
        self.entry_Crop_Right.grid(row=7,column=3)
        #---------------------9行目-----------------------
        text_Crop_Up.grid(row=8,column=0)
        self.entry_Crop_Up.grid(row=8,column=1)
        text_Crop_Down.grid(row=8,column=2)
        self.entry_Crop_Down.grid(row=8,column=3)
        button_Apply_Crop.grid(row=8,column=4)
        #--------------------10行目----------------------
        button_Quit_Setting.grid(row=9,column=0)
        #*------------------------------------------------
    def Toggle_Func(self,event):
        if(event.widget.cget("text") == 'ON'):
            event.widget["text"] = 'OFF'
        elif(event.widget.cget("text") == 'OFF'):
            event.widget["text"] = 'ON'
    def Switch_isSave(self):
        global isSave
        self.isSave = not self.isSave
    def Switch_isMono(self):
        global isMono
        self.isMono = not self.isMono
    def Switch_isGray(self):
        global isGray
        self.isGray = not self.isGray
    def Switch_isResize(self):
        global isResize
        self.isResize = not self.isResize
    def Switch_isCrop(self):
        global isCrop
        self.isCrop = not self.isCrop
    def Apply_Resize(self):
        global resize_width,resize_height
        self.resize_width = self.entry_Resize_Width.get()
        self.resize_height = self.entry_Resize_Height.get()
    def Apply_Crop(self):
        global crop_Left,crop_Right,crop_Up,crop_Down
        self.crop_Left = self.entry_Crop_Left.get()
        self.crop_Right = self.entry_Crop_Right.get()
        self.crop_Up = self.entry_Crop_Up.get()
        self.crop_Down = self.entry_Crop_Down.get()
    def Quit_Setting(self):
        ret = messagebox.askyesno('確認','設定を保存して終了しますか？')
        if(ret == True):
            self.SaveData()
            self.settingWindow.destroy()
    # * -----------------------------------------------------------------

    def create_main(self):
        # * --------------各種ウィジェットの作成-------------------------------
        global entry_SavePath,entry_ImagePath,text_Error
        self.canvas = tk.Canvas(self.frame,bg="white", height=200, width=400)
        text = ttk.Label(self.frame, text='ファイル指定：')
        text_SaveFolder = ttk.Label(self.frame, text='保存先：')
        self.text_Error = ttk.Label(self.frame, text='',foreground='#ff0000')
        self.entry_ImagePath = ttk.Entry(self.frame)
        self.entry_SavePath = ttk.Entry(self.frame)
        button_FileOpen = ttk.Button(self.frame, text='参照', command=lambda:self.OpenImageOnExplorer())
        button_SaveFolderOpen = ttk.Button(self.frame, text='保存先指定', command=lambda:self.OpenSaveFolderOnExplorer())
        button_EditImage = ttk.Button(self.frame, text='編集設定',command=lambda:self.CreateSettingWindow())
        button_Save = ttk.Button(self.frame, text='保存', command=lambda:self.SaveImage())
        button_exit = ttk.Button(self.frame, text='終了', command=lambda:self.ExitApplication())
        # * -----------------各種ウィジェットの設置-----------------------------
        #canvas
        self.canvas.grid(row=0, column=1)
        #raw1 SelectImageFile
        text.grid(row=1, column=0)
        self.entry_ImagePath.grid(row=1, column=1,ipadx=100)
        button_FileOpen.grid(row=1, column=2)
        #raw2 SelectSaveFolder
        text_SaveFolder.grid(row=2, column=0)
        self.entry_SavePath.grid(row=2, column=1,ipadx=100)
        button_SaveFolderOpen.grid(row=2, column=2)
        #raw3 SaveButton
        button_Save.grid(row=3, column=2)
        #raw4 EditSettingWindow & announce
        button_EditImage.grid(row=4, column=2)
        self.text_Error.grid(row=4,column=1)
        #raw5 ExitApplication
        button_exit.grid(row=5,column=0)
    #*----------------------------------------------------------------

Application().main()
