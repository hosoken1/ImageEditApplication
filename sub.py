import json
import os

class AutoSavaImg():
    def __init__(self):
        #設定のロード
        self.setting = self.LoadData()
        #Pathの設定
        self.savePath = '.\Edited'
        self.imgFolderPath = '.\original'
    def __main__(self):
        for file in os.listdir(self.imgFolderPath):
            [fileName, fileExt] = os.path.splitext(file)
            print('file:{} ext:{}'.format(fileName, fileExt))

            if(fileExt != '.jpg' and fileExt != '.png'):
                continue

            #original save
        #if(setting['isSave']==True):
            #img = main.SaveImage()
    def LoadData(self):
        rpath = r'.\savedata.json'
        with open(rpath,"r") as saveData:
            data_dict = json.load(saveData)
            data_json = json.dumps(data_dict)
            print('{}'.format(data_json))
        return data_dict

