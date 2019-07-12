# !/usr/bin/python
# -*- coding: utf-8 -*-


import ssl

# 关闭 ssl 根证书
ssl._create_default_https_context = ssl._create_unverified_context

import time
import requests
import contextlib


def response(url, data, headers):
    try:

        with contextlib.closing(requests.post(url=url, data=data, headers=headers, timeout=30)) as res:
            data = res.json()
        # print("[%s] requests get succ:\n url:%s\n headers:%s\n result:%s\n" % (
        #     now(), url, headers, json.dumps(data).replace("\n", "").replace("\t", "")))
        return "succ", data
    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n headers:%s\n result:%s\n" % (now(), url, headers, ""))
        return "fail", {}


def request_post(url, data, headers):
    try:
        with contextlib.closing(requests.post(url=url, data=data, headers=headers, timeout=30)) as res:
            res_data = res.json()
        # print("[%s] requests get succ:\n url:%s\n params:%s\nheaders:%s\n result:%s\n" % (
        #     now(), url, data, headers, json.dumps(res_data).replace("\n", "").replace("\t", "")))
        return "succ", res_data
    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n params:%s\n headers:%s\n result:%s\nerr:%s" % (
        #     now(), url, data, headers, "", str(e)))
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
        #     now(), url, data, headers, "", str(e)))
        return "fail", {}


def response_get(url, headers):
    try:
        with contextlib.closing(requests.get(url=url, headers=headers)) as res:
            res_data = res.json()
        # print("[%s] requests get succ:\n url:%s\n headers:%s\n result:%s\n" % (
        #     now(), url, headers,
        #     json.dumps(res_data, ensure_ascii=False).replace("\n", "").replace("\t", "").replace(" ", "")))
        return "succ", res_data
    except Exception as e:
        # print("[%s] requests get error:\n url:%s\n headers:%s\n result:%s\n" % (now(), url, headers, ""))
        return "fail", {}


def now():
    return time.strftime("%Y-%m-%d %X")


def get_headers(app_token):
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer %s" % (app_token)
    }
    return headers


def filter_map(params):
    for k in list(params.keys()):
        if not params.get(k, ''):
            params.pop(k)
