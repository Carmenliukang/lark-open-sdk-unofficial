# !/usr/bin/python
# -*- coding: utf-8 -*-


from urllib import parse
from api.Base import Send
from lib.func_txy import filter_map


class GroupManage(Send):
    ''' lark 群操作 '''

    def __init__(self, app_id, app_secret):
        super(GroupManage, self).__init__(app_id=app_id, app_secret=app_secret)
        self.url = "https://open.feishu.cn/open-apis/chat"
        self.version = "v3"

    def get_url(self, method):
        return "%s/%s/%s" % (self.url, self.version, method)

    def group_request(self, url, params={}):
        status, res = self.request(url, params)
        if status == "succ" and str(res.get("code", "")) == "99991663":
            # 用于更新 app_token
            self.update_appinfo()
            status, res = self.request(url, params)
            return status, res
        return status, res

    def create_group(self, name='', description='', open_ids=[], employee_ids=[], i18n_names={}):
        '''
        机器人 创建群组
        :param name:
        :param description:群描述
        :param open_ids:人员列表
        :param employee_ids:人员列表
        :param i18n_names:
        :return:
        '''
        method = "create"
        url = self.get_url(method)
        params = {
            "name": name,
            "description": description,
            "open_ids": open_ids,
            "employee_ids": employee_ids,
            "i18n_names": i18n_names
        }
        filter_map(params)
        return self.group_request(url, params)

    def get_group_list(self, page, page_size):
        '''
        获取群组列表
        :param page:
        :param page_size:
        :return:
        '''
        params = {
            'page': page,
            'page_size': page_size
        }
        method = "list"
        url = self.get_url(method)
        url = "%s?%s" % (url, parse.urlencode(params))
        return self.group_request(url)

    def get_group_info(self, open_chat_id):
        '''获取群信息'''
        params = {
            'open_chat_id': open_chat_id,
        }
        method = "info"
        url = self.get_url(method)
        url = "%s?%s" % (url, parse.urlencode(params))
        return self.group_request(url)

    def group_update(self, open_chat_id="", owner_id="", owner_employee_id="", name="", i18n_names=[]):
        '''更新群信息'''
        method = "update"
        url = self.get_url(method)
        params = {
            'open_chat_id': open_chat_id,
            'owner_id': owner_id,
            'owner_employee_id': owner_employee_id,
            'name': name,
            'i18n_names': i18n_names,
        }
        filter_map(params)

        return self.group_request(url, params)

    def group_add(self, open_chat_id="", open_ids=[], employee_ids=[]):
        '''
        机器人拉人
        :param open_chat_id: 群ID
        :param open_ids: 需要删除的 open_id list
        :param employee_ids: 需要删除的 employee_id
        :return:
        '''
        method = "chatter/add"
        url = self.get_url(method)
        params = {
            'open_chat_id': open_chat_id,
            'open_ids': open_ids,
            'employee_ids': employee_ids,
        }
        filter_map(params)

        return self.group_request(url, params)

    def group_delete(self, open_chat_id="", open_ids=[], employee_ids=[]):
        '''
        机器人删除某人
        :param open_chat_id: 群ID
        :param open_ids: 需要删除的 open_id list
        :param employee_ids: 需要删除的 employee_id
        :return:
        '''
        method = "chatter/delete"
        url = self.get_url(method)
        params = {
            'open_chat_id': open_chat_id,
            'open_ids': open_ids,
            'employee_ids': employee_ids,
        }
        filter_map(params)

        return self.group_request(url, params)
