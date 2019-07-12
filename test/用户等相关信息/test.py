# !/usr/bin/python
# -*- coding: utf-8 -*-

from api.GetInfo import GetBaseInfo

if __name__ == '__main__':
    app_id = 'cli_9c2ecba99aaf910b'
    app_secret = ''
    open_id = ''
    employee_id = ""
    email = ""
    get_base_info = GetBaseInfo(app_id=app_id, app_secret=app_secret)
    print(get_base_info.get_bot_info())
    print(get_base_info.get_user_info_by_employee_id(employee_id))
    print(get_base_info.get_user_info_by_open_id(open_id))
    print(get_base_info.get_user_info_email2id(email=email))
