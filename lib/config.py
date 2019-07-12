# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
读取配置文件中的信息
'''

import configparser
import os


class config(object):
    def __init__(self, filename='../conf/config.conf'):
        self.config = configparser.ConfigParser()
        fp = open(os.path.join(os.path.dirname(__file__), filename))
        self.config.read_file(fp)
        fp.close()

    def setting(self):
        self.setting = {}
        for item in self.config.sections():
            self.setting[item] = self.get_conf(item)
        return self.setting

    def get_conf(self, section):
        setting = {}
        for k, v in self.config.items(section):
            setting[k] = v
        return setting


setting = config().setting()
