# !/usr/bin/python
# -*- coding: utf-8 -*-


from api.Base import Send


class SendMsgOpen(Send):
    ''' 这个是通用的配置，直接可以请求相关的参数的配置 '''

    def __init__(self, app_id, app_secret):
        super(SendMsgOpen, self).__init__(app_id=app_id, app_secret=app_secret)
        self.url = 'https://open.feishu.cn/open-apis/message/v3/send/'
        self.type_dict = {
            'text': 'text',  # 发送文本消息
            'post': 'post',  # 发送富文本消息
            "interactive": "card",  # 发送消息卡片
            'image': 'image_key',  # 发送图片消息
            'share_chat': 'share_open_chat_id',  # 分享群名片
        }

    def get_other_params(self, **kwargs):
        key_list = ['open_id', 'root_id', 'open_chat_id', 'employee_id', 'email']
        params = {}
        for key in key_list:
            if kwargs.get(key):
                params[key] = kwargs.get(key)
        return params

    def get_params_open(self, msg_type, msg, **kwargs):
        '''
        以为 lark open 开放平台这里的接口数据请求格式都是一致的，所以这里可以简化为统一的规范
        :param msg_type: str 枚举 text|post|image|share_chat|interactive
        :param msg: str|dict 具体的格式需要按照相关的参数进行配置
        :param kwargs: dict {"open_id":"","root_id":"","open_chat_id":"","employee_id":""}
        :return: str(succ|fail) dict接口返回的结果
        '''
        msg_type_key = self.type_dict.get(msg_type, '')
        params = {"msg_type": str(msg_type), 'content': {str(msg_type_key): msg}}
        params.update(self.get_other_params(**kwargs))
        return params

    def run(self, msg_type, msg, **kwargs):
        '''
        1. 获取参数
        2. 发送请求
        '''
        params = self.get_params_open(msg_type, msg, **kwargs)
        status, res = self.request(self.url, params)
        if status == "succ" and str(res.get("code", "")) == "99991663":
            self.update_appinfo()
            status, res = self.request(self.url, params)
            return status, res
        return status, res
