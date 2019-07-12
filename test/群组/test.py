# !/usr/bin/python
# -*- coding: utf-8 -*-

from api.Group import GroupManage

if __name__ == '__main__':
    # 这个是直接用来测试的
    app_id = ""
    app_secret = ""
    group_send = GroupManage(app_id, app_secret)

    status, data = group_send.get_group_list(page=1, page_size=100)
