# import sys
#
# sys.path.append("./wechartAPI/api/src")
from .CorpApi import *
from .TestConf import *


# 发送微信企业号消息
def sendmsgbywechart(content, touser="@all", totag="1"):
    ## 创建实例
    api = CorpApi(TestConf['CORP_ID'], TestConf['APP_SECRET'])
    try:
        ## 发送消息
        response = api.httpCall(
            ['/cgi-bin/message/send?access_token=ACCESS_TOKEN', 'POST'],
            {
                "touser": touser,
                # "toparty": toparty,
                "totag": totag,
                "agentid": 1000002,
                'msgtype': 'text',
                'text': {
                    'content': content,
                },
                'safe': 0,
            })
        # print(response['errcode']) errmsg
        return response  # response是<class 'dict'>
    except ApiException as e:
        return str(str(e.errCode) + str(e.errMsg))
