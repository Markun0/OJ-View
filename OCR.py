from os import path
from aip import AipOcr


class BaiduOCR:
    def __init__(self, picfile):
        self.picfile = picfile

    def baiduOCR(self):
        """利用百度api识别文本，并保存提取的文字
        picfile:    图片文件名
        """
        filename = path.basename(self.picfile)
        # 你的AppID，APIKey，Secret Key
        # Mark00, SZtu106094
        APP_ID = '76871832'
        API_KEY = 'iGo7rRQ9n2WsvwJ5NCGOk01p'
        SECRECT_KEY = 'UJEJ9QkxsEFkdDH85AE9NH6SjRAnyVdZ'
        client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

        i = open(self.picfile, 'rb')
        img = i.read()
        print("正在识别图片：\t" + filename)
        # basicGeneral : 通用文字识别
        # basicAccurate : 通用文字识别(高精度版)
        # general : 通用文字识别(含位置信息版)
        # accurate : 通用文字识别(含位置高精度版)
        # enhancedGeneral : 通用文字识别(含生僻字版)
        # webImage : 网络图片文字识别
        message = client.accurate(img)
        # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
        # 打印信息可注释掉，此处是为了调试
        print("识别成功！")
        i.close()
        print(message)
        return message['words_result'][0]['words']

