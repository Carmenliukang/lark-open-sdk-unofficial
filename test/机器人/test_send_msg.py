# !/usr/bin/python
# -*- coding: utf-8 -*-


from api.SendMsg import SendMsgOpen

if __name__ == '__main__':
    app_id = ""
    app_secret = ''

    send_msg_open = SendMsgOpen(app_id=app_id, app_secret=app_secret)

    kwargs = {
        "email": ""
    }

    msg_type_dict = {
        'text': 'text',
        'post': 'post',
        'image': 'image_key',
        'share_chat': 'share_open_chat_id',
        "interactive": "card"
    }

    status, res = send_msg_open.run('text', "", **kwargs)
