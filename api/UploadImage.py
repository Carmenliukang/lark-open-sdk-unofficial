# !/usr/bin/python
# -*- coding: utf-8 -*-


from api.Base import Send


class UploadImage(Send):
    '''
    用于上传图片
    '''

    def __init__(self, app_id, app_secret):
        super(UploadImage, self).__init__(app_id, app_secret)
        self.url = "https://open.feishu.cn/open-apis/image/v3/upload/"

    def run(self, file_name=""):
        try:
            with open(file_name, 'rb') as f:
                image = f.read()
            files = {'image': image}
            return self.request_post_file(self.url, files)
        except:
            return "fail", ""
