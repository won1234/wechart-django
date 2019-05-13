#!/usr/bin/env python
# -*- coding:utf-8 -*-
##
# Copyright (C) 2018 All rights reserved.
#
# @File UserTest.py
# @Brief
# @Author abelzhu, abelzhu@tencent.com
# @Version 1.0
# @Date 2018-02-24
#
#

import sys

sys.path.append("../src/")

import random

from CorpApi import *

from TestConf import *

## test
api = CorpApi(TestConf['CORP_ID'], TestConf['APP_SECRET'])

try:
    ## 发送消息
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            # "touser": "@all",
            # "toparty": "2",
            "totag": "1",
            "agentid": 1000002,
            'msgtype': 'text',
            'text': {
                'content': '方法论6\n方法',
            },
            'safe': 0,
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)
