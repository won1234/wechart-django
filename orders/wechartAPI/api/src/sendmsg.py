# import sys
#
# sys.path.append("./wechartAPI/api/src")
from .CorpApi import *
from .TestConf import *
from login.models import Profile


# 发送微信企业号消息
def test(msg):
    ## 创建实例
    api1 = CorpApi(TestConf['CORP_ID'], '7_f86lX3DaLpFGKW_Ya6WvKe-QQVKlkjVr5fp0N8cHQ')
    # 发送给tag的消息
    api2 = CorpApi(TestConf['CORP_ID'], TestConf['APP_SECRET'])
    try:
        ## 发送消息
        response = api2.httpCall(
            ['/cgi-bin/message/send?access_token=ACCESS_TOKEN', 'POST'],
            {
                # "touser": wechat_name,
                # "toparty": toparty,
                "totag": 1,
                "agentid": 1000002,
                'msgtype': 'text',
                'text': {
                    'content': msg,
                },
                'safe': 0,
            })
        # print(response['errcode']) errmsg
        return response  # response是<class 'dict'>
    except ApiException as e:
        return str(str(e.errCode) + str(e.errMsg))

# 发送微信企业号消息
def sendmsgbywechart(user_profile, message_user, message_tag):
    ## 创建实例
    api1 = CorpApi(TestConf['CORP_ID'], '7_f86lX3DaLpFGKW_Ya6WvKe-QQVKlkjVr5fp0N8cHQ')
    # 取得用户的企业号个人账号
    wechat_name = user_profile.wechat_name
    if not wechat_name:        # 如果为空，发送给管理员
        wechat_name = 'WuGuangQiang'
    # 发送给下单的人的消息
    try:
        ## 发送消息
        response = api1.httpCall(
            ['/cgi-bin/message/send?access_token=ACCESS_TOKEN', 'POST'],
            {
                "touser": wechat_name,
                # "toparty": toparty,
                # "totag": totag,
                "agentid": 1000003,
                'msgtype': 'text',
                'text': {
                    'content': message_user,
                },
                'safe': 0,
            })
        # print(response['errcode']) errmsg
        # return response  # response是<class 'dict'>
    except ApiException as e:
        # return str(str(e.errCode) + str(e.errMsg))
        pass

    # 发送给tag的消息
    api2 = CorpApi(TestConf['CORP_ID'], TestConf['APP_SECRET'])
    try:
        ## 发送消息
        response = api2.httpCall(
            ['/cgi-bin/message/send?access_token=ACCESS_TOKEN', 'POST'],
            {
                # "touser": wechat_name,
                # "toparty": toparty,
                "totag": 1,
                "agentid": 1000002,
                'msgtype': 'text',
                'text': {
                    'content': message_tag,
                },
                'safe': 0,
            })
        # print(response['errcode']) errmsg
        return response  # response是<class 'dict'>
    except ApiException as e:
        return str(str(e.errCode) + str(e.errMsg))
