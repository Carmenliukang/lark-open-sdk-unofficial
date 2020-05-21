# !/usr/bin/python
# -*- coding: utf-8 -*-

from api.Base import Send


class SendMsgOpen(Send):
    ''' 这个是通用的配置，直接可以请求相关的参数的配置 '''

    def __init__(self, app_id, app_secret):
        super(SendMsgOpen, self).__init__(app_id=app_id, app_secret=app_secret)
        self.url = 'https://open.feishu.cn/open-apis/message/v4/send/'
        self.type_dict = {
            'text': 'text',  # 发送文本消息
            'post': 'post',  # 发送富文本消息
            "interactive": "card",  # 发送消息卡片
            'image': 'image_key',  # 发送图片消息
            'share_chat': 'share_chat_id',  # 分享群名片
        }

    def get_other_params(self, **kwargs):
        key_list = ['open_id', 'root_id', 'open_chat_id', 'employee_id', 'email', "user_id", "chat_id"]
        params = {}
        for key in key_list:
            if kwargs.get(key):
                if key == "open_chat_id":
                    params["chat_id"] = kwargs.get(key)
                elif key == "employee_id":
                    params["user_id"] = kwargs.get(key)
                else:
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
        if msg_type != 'interactive':
            msg_type_key = self.type_dict.get(msg_type, '')
            params = {"msg_type": str(msg_type), 'content': {str(msg_type_key): msg}}
            params.update(self.get_other_params(**kwargs))
            return params
        else:
            params = {"msg_type": str(msg_type), 'card': msg}
            params.update(self.get_other_params(**kwargs))
            return params

    def run(self, msg_type, msg, **kwargs):
        '''
        1. 获取参数
        2. 发送请求
        3. 兼容 卡片消息 最新版本
        '''
        params = self.get_params_open(msg_type, msg, **kwargs)
        status, res = self.request(self.url, params)
        if status == "succ" and str(res.get("code", "")) == "99991663":
            self.update_appinfo()
            status, res = self.request(self.url, params)
            return status, res
        return status, res


class SendUrgentMsg(Send):
    '''
    用于发送加急的数据,这里是用于修改的
    '''

    def __init__(self, app_id, app_secret):
        super(SendUrgentMsg, self).__init__(app_id, app_secret)
        self.url = "https://open.feishu.cn/open-apis/message/v4/urgent/"

    def run(self, open_message_id, urgent_type, open_ids):
        if len(open_ids) <= 50:
            return self.open_ids_post(open_message_id, urgent_type, open_ids)
        else:
            return self.open_ids_split_post(open_message_id, urgent_type, open_ids)

    def open_ids_post(self, open_message_id, urgent_type, open_ids):
        data = {
            'message_id': open_message_id,  # 消息ID，指定该参数针对某条消息进行加急，发送消息后返回
            "urgent_type": urgent_type,  # 加急类型。目前支持应用内加急(app)，短信加急(sms)，电话加急(phone)。加急权限需要申请。
            "open_ids": open_ids,  # 用户标识，指定该参数向指定用户发加急消息
        }
        self.filter_map(data)
        status, res = self.request(self.url, data)
        if status == "succ":
            if str(res.get("code", "")) == "99991663":
                self.update_appinfo()
                status, res = self.request(self.url, data)

        return status, res

    def open_ids_split_post(self, open_message_id, urgent_type, open_ids):
        open_ids_len = len(open_ids)
        aplit_num = open_ids_len / 50
        if open_ids_len % 50 != 0:
            aplit_num = aplit_num + 1

        for i in range(0, int(aplit_num)):
            start = int(50 * i)
            end = int(50 * (i + 1))
            status, res = self.open_ids_post(open_message_id, urgent_type, open_ids[start:end])

        return status, res
