#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ssl

# 关闭 ssl 根证书
ssl._create_default_https_context = ssl._create_unverified_context

import time
import json
import requests
import contextlib


class Base(object):
    ''' 授权基类 '''

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

    def request(self, url, msg=""):
        '''
        请求接口，获取返回的数值
        :param msg: dict {"url":"","params":""}
        :param app_token: app token 刷新
        :return: string dict
        '''
        if msg:
            params = json.dumps(msg)
            headers = get_headers(self.app_token)
            status, res = self.post(url, params, headers)
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

    def request_delete(self, url, msg=""):
        '''
        请求接口，获取返回的数值
        :param msg: dict {"url":"","params":""}
        :param app_token: app token 刷新
        :return: string dict
        '''
        if msg:
            params = json.dumps(msg)
        else:
            params = msg
        headers = get_headers(self.app_token)
        status, res = self.delete(url, params, headers)
        return status, res

    def request_patch(self, url, msg=""):
        '''
        请求接口，获取返回的数值
        :param msg: dict {"url":"","params":""}
        :param app_token: app token 刷新
        :return: string dict
        '''
        params = json.dumps(msg)
        headers = get_headers(self.app_token)
        status, res = self.patch(url, params, headers)
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

    def delete(self, url, params, headers):
        status, res = response_delete(url, params, headers)
        return status, res

    def patch(self, url, params, headers):
        status, res = response_patch(url, params, headers)
        return status, res

    def filter_map(self, params):
        for k in list(params.keys()):
            if not params.get(k, ''):
                params.pop(k)


def request_get(url):
    try:
        with contextlib.closing(requests.get(url)) as req:
            content = req.content
        return "succ", content
    except Exception as e:
        print(e)
        return "fail", ""


def response(url, data, headers):
    try:

        with contextlib.closing(requests.post(url=url, data=data, headers=headers, timeout=30)) as res:
            data = res.json()
        # print("[%s] requests get succ:\n url:%s\n headers:%s\n result:%s\n" % (
        #     now(), url, headers, json.dumps(data).replace("\n", "").replace("\t", "")))
        return "succ", data
    except Exception as e:
        print("[%s] requests get error:\n url:%s\n headers:%s\n result:%s\n" % (now(), url, headers, ""))
        return "fail", ""


def response_get(url, headers):
    try:

        with contextlib.closing(requests.get(url=url, headers=headers)) as res:
            data = res.json()
        # print("[%s] requests get succ:\n url:%s\n headers:%s\n result:%s\n" % (
        #     now(), url, headers, data.replace("\n", "").replace("\t", "").replace(" ", "")))
        return "succ", data
    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n headers:%s\n result:%s\n" % (now(), url, headers, ""))
        return "fail", ""


def response_get_params(url, params, headers):
    try:

        with contextlib.closing(requests.get(url=url, params=params, headers=headers)) as res:
            data = res.json()
        return "succ", data
    except Exception as e:
        print("[%s] requests get error:\n url:%s\n headers:%s\n result:%s\n" % (now(), url, headers, ""))
        return "fail", {}


def request_post(url, data, headers):
    try:

        with contextlib.closing(requests.post(url=url, data=data, headers=headers, timeout=30)) as res:
            res_data = res.json()

        return "succ", res_data
    except Exception as e:
        print(e)
        return "fail", {}


def request_post_file(url, files, headers):
    try:

        with contextlib.closing(requests.post(url=url, files=files, headers=headers, timeout=30, stream=True)) as res:
            res_data = res.json()

        # print("[%s] requests get succ:\n url:%s\n \nheaders:%s\n result:%s\n" % (
        #     now(), url, headers, json.dumps(res_data).replace("\n", "").replace("\t", "")))
        return "succ", res_data
    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n params:%s\n headers:%s\n result:%s\nerr:%s" % (
        #     now(), url, "", headers, "", str(e)))
        return "fail", {}


def response_delete(url, data, headers):
    try:
        if data:
            with contextlib.closing(requests.delete(url=url, data=data, headers=headers)) as res:
                res_data = res.json()
            # print("[%s] requests get succ:\n url:%s\n params:%s\n headers:%s\n result:%s\n" % (
            #     now(), url, data, headers, json.dumps(res_data).replace("\n", "").replace("\t", "").replace(" ", "")))
            return "succ", res_data
        else:
            with contextlib.closing(requests.delete(url=url, headers=headers)) as res:
                res_data = res.json()
            # print("[%s] requests get succ:\n url:%s\n headers:%s\n result:%s\n" % (now(), url, headers, data))
            return "succ", res_data

    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n params:%s headers:%s\n result:%s\n err:%s" % (
        #     now(), url, data, headers, "", str(e)))
        return "fail", {}


def response_patch(url, data, headers):
    try:
        with contextlib.closing(requests.patch(url=url, data=data, headers=headers)) as res:
            res_data = res.json()
        # print("[%s] requests get succ:\n url:%s\n params:%s headers:%s\n result:%s\n" % (
        #     now(), url, data, headers, data.replace("\n", "").replace("\t", "").replace(" ", "")))
        return "succ", res_data
    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n headers:%s\n result:%s\n err:%s" % (now(), url, headers, "", str(e)))
        return "fail", ""


def now():
    return time.strftime("%Y-%m-%d %X")


def get_headers(app_token):
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer %s" % (app_token)
    }
    return headers
