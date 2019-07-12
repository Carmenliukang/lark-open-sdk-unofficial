# !/usr/bin/python
# -*- coding: utf-8 -*-

import json
from lib.func_txy import *


class Send(object):
    ''' SDK 基类 包含 URL 请求 app_token 更新通过 redis 或者 MySQL 查询 '''

    def __init__(self, app_id, app_secret):
        self.fresh_url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/'
        self.app_id = app_id
        self.app_secret = app_secret
        self.fresh_token()

    def fresh_token(self):
        headers = {"content-type": "application/json"}
        data = json.dumps({"app_id": self.app_id, "app_secret": self.app_secret})
        status, res = response(self.fresh_url, data, headers)
        self.app_token = res.get("tenant_access_token", "")

    def update_appinfo(self):
        self.fresh_token()

    def request(self, url, params=""):
        '''
        请求接口，获取返回的数值
        :param msg: dict {"url":"","params":""}
        :param app_token: app token 刷新
        :return: string dict
        '''
        if params:
            params_res = json.dumps(params)
            headers = get_headers(self.app_token)
            status, res = self.post(url, params_res, headers)

        else:
            headers = get_headers(self.app_token)
            status, res = self.get(url, headers)

        return status, res

    def request_post_file(self, url, files=""):
        '''
        请求接口，获取返回的数值
        :param msg: dict {"url":"","params":""}
        :param app_token: app token 刷新
        :return: string dict
        '''
        headers = {'Authorization': "Bearer %s" % (self.app_token)}
        status, res = self.post_file(url, files, headers)

        return status, res

    def request_app_token(self, msg, app_token):
        '''
        请求接口，获取返回的数值
        :param msg: dict {"url":"","params":""}
        :param app_token: app token 刷新
        :return: string dict
        '''
        url = msg.get("url", "")
        params = msg.get('params', '')
        headers = get_headers(app_token)
        status, res = self.post(url, params, headers)
        return status, res

    def post_file(self, url, files, headers):
        status, res = request_post_file(url, files, headers)
        return status, res

    def post(self, url, params, headers):
        status, res = request_post(url, params, headers)
        return status, res

    def get(self, url, headers):
        status, res = response_get(url, headers)
        return status, res
