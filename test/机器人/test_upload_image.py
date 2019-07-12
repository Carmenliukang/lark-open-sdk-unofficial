# !/usr/bin/python
# -*- coding: utf-8 -*-

from api.UploadImage import UploadImage

if __name__ == '__main__':
    app_id = ""
    app_secret = ''
    update_image = UploadImage(app_id=app_id, app_secret=app_secret)
    print(update_image.run(file_name=""))
