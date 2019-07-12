# !/usr/bin/python
# -*- coding: utf-8 -*-


from urllib import parse
from api.Base import Send
from lib.func_txy import filter_map


class GetBaseInfo(Send):
    ''' 获取相关的URL的修改 '''

    def __init__(self, app_id, app_secret):
        super(GetBaseInfo, self).__init__(app_id=app_id, app_secret=app_secret)
        self.url = 'https://open.feishu.cn/open-apis/user'
        self.version = "v3"

    def get_url(self, method):
        '''
        获取请求URL，按照 url + version + method 修改
        :param method: method
        :return: str url
        '''
        return "%s/%s/%s/" % (self.url, self.version, method)

    def user_request(self, url, params={}):
        '''
        url get 、 post 请求,同时通过判断 token 是否过期，进行更新 token
        :param url:
        :param params: 如果 为 "",{} 等 if 判断 为 False 则为 get 请求
        :return: string ("succ"|"fail") dict 返回请求的结果
        '''
        status, res = self.request(url, params)
        if status == "succ" and str(res.get("code", "")) == "99991663":
            # 用于更新 app_token
            self.update_appinfo()
            status, res = self.request(url, params)
            return status, res
        return status, res

    def get_user_info_by_open_id(self, open_id=''):
        '''
        通过 openi_id 获取个人信息
        :param open_id: open_id
        :return:
        '''
        method = "info"
        url = self.get_url(method)
        params = {
            "open_id": open_id,
        }
        filter_map(params)
        url = "%s?%s" % (url, parse.urlencode(params))

        return self.user_request(url)

    def get_user_info_by_employee_id(self, employee_id=''):
        '''
        通过 employee_id 获取个人的信息
        :param employee_id:
        :return:
        '''
        method = "info"
        url = self.get_url(method)
        params = {
            "employee_id": employee_id,
        }
        filter_map(params)
        url = "%s?%s" % (url, parse.urlencode(params))

        return self.user_request(url)

    def get_user_info_email2id(self, email=''):
        '''
        将 email 邮箱转换成open_id 等其他的信息
        :param email:
        :return:
        '''
        method = "email2id"
        url = self.get_url(method)
        params = {
            "email": email,
        }
        filter_map(params)

        return self.user_request(url, params)

    def get_bot_info(self):
        ''' 获取机器人相关信息 '''
        url = 'https://open.feishu.cn/open-apis/bot/v3/info/'
        return self.user_request(url)
