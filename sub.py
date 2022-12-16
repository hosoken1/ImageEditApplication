import json
from PIL import Image
import os

class AutoSavaImg():
    def __init__(self):
        #設定のロード
        self.setting = self.LoadData()
        #pathの設定
        self.savePath = 'Edited'
        self.imgFolderPath = 'original'
    def __main__(self):
        for file in os.listdir(self.imgFolderPath):
            fileBaseName = os.path.basename(file)
            [fileName, fileExt] = os.path.splitext(file)
            print('file:{} ext:{}'.format(fileName, fileExt))
            #拡張子のチェック
            if(fileExt != '.jpg' and fileExt != '.png'):
                continue
            #画像の読み込み
            img = Image.open(self.imgFolderPath + '/' + fileName + fileExt)
            currentSavePath = self.savePath
            #original save
            if(self.setting['isSave']==True):
                savePath_Original = self.savePath + '/' + fileName + fileExt
                img.save(savePath_Original ,quality=90)
            if(self.setting['isMono']==True):
                img_Mono = self.EditImageMono(img)
                savePath_Mono = currentSavePath + '/' + fileName + '_mono' + fileExt
                img_Mono.save(savePath_Mono ,quality=90)
            if(self.setting['isGray']==True):
                img_Gray = self.EditImageGray(img)
                savePath_Gray = currentSavePath + '/' + fileName + '_gray' + fileExt
                img_Gray.save(savePath_Gray ,quality=90)
            if(self.setting['isResize']==True):
                img_Resize = self.EditImageResize(img)
                savePath_Resize = currentSavePath + '/' + fileName + '_resize' + fileExt
                img_Resize.save(savePath_Resize ,quality=90)
            if(self.setting['isCrop']==True):
                img_Crop = self.EditImageCrop(img)
                savePath_Crop = currentSavePath + '/' + fileName + '_crop' + fileExt
                img_Crop.save(savePath_Crop ,quality=90)

    #モノクロ
    def EditImageMono(self,_img):
        _img_mono = _img.convert(mode='1')
        return _img_mono
    #グレー
    def EditImageGray(self,_img):
        _img_mono = _img.convert(mode='L')
        return _img_mono
    #リサイズ
    def EditImageResize(self,_img):
        width = int(self.setting['resize_width'])
        height = int(self.setting['resize_height'])
        print('width: {}, height: {}'.format(width, height))
        _img_resized = _img.resize((width,height))
        return _img_resized
    #切り抜き
    def EditImageCrop(self,_img):
        left = int(self.setting['crop_Left'])
        right = int(self.setting['crop_Right'])
        up = int(self.setting['crop_Up'])
        down = int(self.setting['crop_Down'])
        print('left: {}, right: {}, up: {}, down:{}'.format(left,right,up,down))
        _img_croped = _img.crop((left,up,right,down))
        return _img_croped

    def LoadData(self):
        rpath = 'savedata.json'
        with open(rpath,"r") as saveData:
            data_dict = json.load(saveData)
            data_json = json.dumps(data_dict)
            print('{}'.format(data_json))
        return data_dict
AutoSavaImg().__main__()
