#!/usr/bin/env python
#  用于测试发送消息


import sys

sys.path.append("../src/")
from CorpApi import *

# 获取 accessToken
#   https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRECT
TestConf = {

    # 企业的id，在管理端->"我的企业" 可以看到
    "CORP_ID": "ww87bc66fe6a7a7ac7",

    # 某个自建应用的id及secret, 在管理端 -> 企业应用 -> 自建应用, 点进相应应用可以看到
    "APP_ID": 1000002,
    "APP_SECRET": "B353C69-O9d5wSpC5Oq9j8ggIY84z0TwlVAd9nod0TE",

}

# url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + TestConf["CORP_ID"] + '&corpsecret=' + TestConf["APP_SECRET"]
# print(url)

api = CorpApi(TestConf['CORP_ID'], TestConf['APP_SECRET'])

# 发送消息
try:
    ##
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            "touser": "UserID1|UserID2|UserID3",
            "toparty": "PartyID1|PartyID2",
            "totag": "TagID1 | TagID2",
            "msgtype": "text",
            "agentid": 1,
            "text": {
                "content": "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
            },
            "safe": 0
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)
