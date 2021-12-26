# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/20 13:25
@Auth ： maomao
@File ：maomao_didi_ql.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

'''参考了zyf1118的浏览代码，感谢那位大佬！'''

'''
cron: 0 0-23/10 * * *
new Env('滴滴盲盒');
'''

'''
wsgsig 的值可以忽略
https://game.xiaojukeji.com/api/game/plant/?????
'''
import requests

requests.urllib3.disable_warnings()
import re
import json
import os
import sys

import datetime
import time

import random

nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f8')
today = datetime.datetime.now().strftime('%Y-%m-%d')
time1 = '08:00:00.00000000'
time2 = '12:00:00.00000000'
time3 = '15:00:00.00000000'
time4 = '17:00:00.00000000'
get_time1 = '{} {}'.format(today, time1)
get_time2 = '{} {}'.format(today, time2)
get_time3 = '{} {}'.format(today, time3)
get_time4 = '{} {}'.format(today, time4)

wsgsig = [
    'dd03-vx9tq2onDp0IZqcYVoABxTjsa%2BXNwlstUQ6fOSmVa%2BX%2BZhfRmNkDw6zkAz0%2BZA8rsJ2%2BzMKjCoJLpecxVoEAOMK%2FBzf2SAJmXo6ax6Nre%2BnNYVNkX72aP6KjAJE',
    'dd03-67TGcdCHNXqCW0FVDMhX%2B%2F%2B650AFtbkyCIqj4r3350AEWfAm9TIW%2B9cKMnqEWXIwEPUQLAXc%2BWT0%2FiFqd1%2Fn%2Be36LslfUXIyD61n%2BAgNL096XnZxBMZUNl%2BN%2BXO',
    'dd03-rxqml47pGugrvrGTzy%2FbOp8ud3nWyknnyQTDxoGxd3nXv%2FDzSNEfP8%2BSFQgXvBJlYJP3Q%2BvlFR3UTdGPxKw9RJGuE3%2BtZa8rPod9xp3uF3KrvEbhPolCP3KkEQ9',
    'dd03-%2FbmamzeJR3QXGQJTThyOOv18ZuJqDzvOpFvUyJM1ZuJrGv%2BqxrbhQvEIOJQrGJGQPVzxPRAHQ3WnfpjwpEQmzRLaPJyXE%2BcyYhyiy763PujiGJiPSrWnRN28xJQV',
    'dd03-UfTkqudHf%2B4nfF8UZV2awyM6Epv%2Fc9oqvBqBO%2BL3Epvhfd3OPVIdwyFKe84hfVcsxrU1zoBJg%2BKXGAWkvAwBxo2KBQgPfebhZqxdwRMHB%2BcjfF%2BtuFhMxReNd3Ct',
    'dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY',
    'dd03-aScF%2FD3Xy4FqxzWqMzcXogciSvVXYQRtNv7%2FYmClSvVWxo8R58nVS0KUxKFWx8frH43PpggVz3HVRJ3x2z8wYgNlxR6yPzfqM%2BNhZg7%2FzKHjx3Nr2z7kTXDVwKE',
    'dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY',
    'dd03-NEvAAAqxzcF7%2B%2B%2Fqb0pV6dhOTjV2J3xtacmlHlYpTjV1%2B7IRDn8q5EhywDF1%2BpArgjiS8drvwbH42uLxbbRXIkhWyD5M4z1rb0ok6hZWwjl4MpFhcnXVIalvPDH',
    'dd03-DUXVE0SysCEZ%2BS1O7nX62jMR%2FsUyJZPj5jQ9LikS%2FsUz%2Bx6vNgDF1DxxrbEz%2BLdh3coI4cPvqjIw221TJXgA1tVvlnaPM2APJXba1tURrbhPMLBt7ntC1DhYks9',
    'dd03-wDXIwYa7Z54GDovErARRsS5KRwvBGvJAtdQwkMILRwvADzyHh%2FDPqwA6uL4ADNnCVkoVtSd5vMfDe4v7sevTrwh%2Bu5baf4zBrAXPqLEEYICcD7j3kqcRsSA4YL1',
    'dd03-y3uI01tMPCX7nJYRt2No3SQ1vs02i8IprMnw%2BTv8vs01n4xXjP7P45iNQbX1nQkTXTjV1LW%2BRcQ4rzYhq5iP42QgRgRBt8xzsZmQ%2BSj3O0R8t3PzsSs%2F4SWLyCq',
    'dd03-%2Fep12zdOxaJXJ8w9TGpxE42xphQq%2BJMdpCsTaJLuphQrJNZ5xWKYFvFRyBJrJz%2FfPsWkGRapzA0s5QwJTjQSFKAzRhci73VGSjvvFK9zzkgl7%2BYgoDuPaoLzRaL',
    'dd03-z6%2BZsOikr8p3Z5vssNK6z5jrjz%2B6wIJZqJCLQ6QWjz%2B5ZMyhioR2yStns%2Bp5ZwnvWQGexwnmtNs8pPvXsv87yZnnm3n6T2oPtNbMzwtlnJj6vwGPsRbKzwgonJk',
    'dd03-0%2F1PtGPrF8UO5avU3tAazsYkgzEp2EJz1Xe5RjhjgzEo5AynJDwIzCYsG%2BUo5hnx70aFwbSt0NPTJUvr3fHNzgSsb3wpHdop4tF6ybYqcJYp7hGp3GF4ybLvcJw',
    'dd03-rDByxRBD9w%2BsAUn7w966q%2BEfC5pVFhGFydLKl72aC5pUAliMS%2FV7rp9AcS%2BUAEv0YkHbszEBbTCXfan4wVa2ruEA0ZgVdrsex95Jqz9CGPcVCEJewl5LqzU2GPd',
    'dd03-gUaMGbSXHChPMWOhInVo1fTi3saoHj2QHj5YNXkl3sapMnTs3glT3fxUKbhpMGUONc1r2GPqJcwS4cOkKbHv1fMV8sVQLW9Q8nBlNWIUKiYwLWSoIsEz%2BfOhJXq',
    'dd03-ZB27DIBhLttb1gkuUiIX8TLU7DDe6CFyWfdRKw2t7DDd1Ghmkixy8M9i%2Bjtd1nYwqm9i56EmNiogNskqUgESKTBU%2BfiC1glSUnHO8xBr3DbG2ihpUgIW76Um3jq',
    'dd03-20QwPlA2%2FILbbHoaEks8lhBLsPSeg68eG9XIrA1KsPSdb2R6dkN5lha3j2LdbOsgA%2Ft9mrF7i1BgExoK9dzMldHNWIIA9TWN9ao2qkICWL9ebHs%2B0d71khHIiL5',
    'dd03-35eouVsWdxONxlnc0%2BaNWavjG6HIYqGHFK14i9ukG6HHxUiAgphNWrjVgTOHxevJDR5CVhXrfSVKRAnf0QMHUURrg1x6OF%2BcE3H4iaujgYkaOFpcbQA8WrnqgHY',
    'dd03-qRg6qKKGw8DUhpRWx14yy%2BGcozttku3szw3OOycdoztshyoQT1jxw%2B3Fz%2BDsh%2BXqZ57hz8NBzoNrX3RwPYNpxuNERz8tUztXwOsOxQbCzuf%2FV3nWx1sSy%2BJGx%2BE',
    'dd03-zzyKkOo5PQ82t3sQsSuQOLnIvJz7W%2BchqOjyw6mNvJz8tKXZiL3ROSz8Qu88tuojWHnXRwR5QRb5lpspswWSQSJNQJc4tzultPnYx5R3QzKGrzzrswzuw2v8zQd',
    'dd03-XGGZ8J%2FbhAtQdOYFue33BNV0tqDTaxI7YaKLgzOAtqDSdZxfQls2DNrai9tSdHk5yh%2BeA7ldiaopC6YAue4JB7SA%2FAtkf1rLulKLfyqCWVnldOTKul4KgvYC%2F9S',
    'dd03-DOgz5gRWq%2FAYTS%2F26v82Acsji9qzOZBC5z3Jdsjki9qyTxlJN4j8AcuVtqAyTLwA387cDDoXsrMxv2%2F5KKfKAfX%2Fs9HyTIYG8NK0BtnjrV5uZ5LDJvfKAWWUrq5',
    'dd03-kQNDYoKdpT7kl4cdP27UVJJBxMyj%2FNsaRxDm%2F4cGxMyilJf2Z2QtUQ3gSx7ilv8cT60pXuNdSwchtoc%2BPINqUJcETYN%2Fr7DdOSbqU3JgTO%2BqrRJEQP%2B%2FV%2BbfSTd',
    'dd03-RnANOxOD1Z3H9sJdnUHQlIrfJ2u%2Ben09kqMvqH%2FaJ2uN9jj1WEUokZZA4P3N9CubiAIsnPrD4OgMGgmNmd5plZPCN2NIF0zGlUBwqLxCNPNHaitCnE6xlZqa2ZA'
]

sys.path.append('../../tmp')
sys.path.append(os.path.abspath('.'))
try:
    import requests
except Exception as e:
    msg(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")

run_send = 'yes'  # yes或no, yes则启用通知推送服务

'''———————————————————————pycharm环境——————————————————————————————'''

# with open('12test', 'r') as f2:
#     token = f2.read()

'''———————————————————————pycharm环境——————————————————————————————'''

'''———————————————————————ql环境——————————————————————————————'''

with open(r'/ql/config/djangolog/diditoken.txt', 'r') as f2:
    token = f2.read()


'''———————————————————————ql环境——————————————————————————————'''

# 读取所有的token 给到tokenpro

token_re = re.findall('\"(.*)\"', token)


def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# 将重复的token给到token_re （list形式）
token_re = getUniqueItems(token_re)


## 获取通知服务
class Msg(object):
    def getsendNotify(self):
        url_list = [
            'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
            'https://cdn.jsdelivr.net/gh/wuye999/myScripts@main/sendNotify.py',
            'https://raw.fastgit.org/wuye999/myScripts/main/sendNotify.py',
            'https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
        ]
        for e, url in enumerate(url_list):
            try:
                response = requests.get(url, timeout=10)
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
                return
            except:
                if e >= (len(url_list) - 1):
                    msg('获取通知服务失败，请检查网络连接...')

    def main(self, f=0):
        global send, msg, initialize
        sys.path.append(os.path.abspath('.'))
        for _ in range(2):
            try:
                from sendNotify import send, msg, initialize
                break
            except:
                self.getsendNotify()
        l = ['BARK_PUSH', 'BARK_ARCHIVE', 'BARK_GROUP', 'BARK_SOUND', 'DD_BOT_SECRET', 'DD_BOT_TOKEN', 'FSKEY',
             'GOBOT_URL', 'GOBOT_QQ', 'GOBOT_TOKEN', 'GOTIFY_URL', 'GOTIFY_TOKEN', 'GOTIFY_PRIORITY', 'IGOT_PUSH_KEY',
             'PUSH_KEY', 'PUSH_PLUS_TOKEN', 'PUSH_PLUS_USER', 'QMSG_KEY', 'QMSG_TYPE', 'QYWX_AM', 'QYWX_KEY',
             'TG_BOT_TOKEN', 'TG_USER_ID', 'TG_API_HOST', 'TG_PROXY_AUTH', 'TG_PROXY_HOST', 'TG_PROXY_PORT']
        d = {}
        for a in l:
            try:
                d[a] = eval(a)
            except:
                d[a] = ''
        try:
            initialize(d)
        except:
            if f < 2:
                f += 1
                self.getsendNotify()
            if f < 5:
                f += 1
                return self.main(f)
            else:
                msg('获取通知服务失败，请检查网络连接...')


Msg().main()  # 初始化通知服务

a = ''


def get_xpsid():
    try:
        url = f'https://v.didi.cn/p/DpzAd35?appid=10000&lang=zh-CN&clientType=1&trip_cityid=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&channel=102&appversion=6.2.4&trip_country=CN&TripCountry=CN&lng=113.812538&maptype=soso&os=iOS&utc_offset=480&access_key_id=1&deviceid=99d8f16bacaef4eef6c151bcdfa095f0&phone=UCvMSok42+5+tfafkxMn+A==&model=iPhone11&lat=23.016271&origin_id=1&client_type=1&terminal_id=1&sig=8503d986c0349e40ea10ff360f75d208c78c989a'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head(url=url, headers=heards, verify=False)  # 获取响应请求头
        res = response.headers['Location']  # 获取响应请求头
        # msg(res)
        r = re.compile(r'root_xpsid=(.*?)&appid', re.M | re.S | re.I)
        xpsid = r.findall(res)
        xpsid = xpsid[0]
        return xpsid
    except Exception as e:
        msg(e)
        msg("获取xpsid失败，可能是表达式错误")


# 浏览
def manghe_liulan(token, xpsid):
    for _ in range(5):
        url = f'https://ut.xiaojukeji.com/ut/welfare/api/blindBox/reportBrowseTask'
        heards = {
            'Accept': 'application/json, text/plain, */*',
            "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
            "Content-Type": "application/json",
        }
        data = {
            "xbiz": "240400",
            "prod_key": "vendor",
            "xpsid": f"{xpsid}",
            "dchn": "nr1on9k",
            "xoid": "VIdBMwzuSpa8IPNX9Y3Bzg",
            "uid": "286475020565532",
            "xenv": "passenger",
            "xspm_from": "",
            "xpsid_root": "e418afe8f0d94887a338140eb0355c49",
            "xpsid_from": "",
            "xpsid_share": "",
            "token": token,
            "platform": "na",
            "lng": "116.12943549262152",
            "lat": "24.33239013671875",
            "group": "0",
            "env": "{\"xAxes\":305,\"yAxes\":404,\"isHitButton\":true}"
        }
        json_str = json.dumps(data)
        response = requests.post(url=url, headers=heards, verify=False, data=json_str)
        msg(response.text)
        data = json.loads(response.text)
        time.sleep(4)
        errmsg = data['errmsg']
        if errmsg == 'success':
            msg('浏览成功！')
        else:
            msg('浏览失败！')


# 今日访问
def manghe_fangwen(token, xpsid, wsgsig):
    id = wsgsig[random.randint(0, 25)]
    url = f'https://ut.xiaojukeji.com/ut/welfare/api/blindBox/getPopup?wsgsig={id}'
    heards = {
        "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x1800103b) NetType/WIFI Language/zh_CN miniProgram',

        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = {
        "xbiz": "240400",
        "prod_key": "vendor",
        "xpsid": f"{xpsid}",
        "dchn": "Ep9b0kx",
        "xoid": "5781c9a1-f3ca-4c29-9e7b-e95df2397dab",
        "uid": "283726966498823",
        "xenv": "wxmp",
        "xspm_from": "none.none.none.none",
        "xpsid_root": "2679b899c5634c8b902ddbf448d5dba3",
        "xpsid_from": "",
        "xpsid_share": "",
        "token": f"{token}",
        "platform": "mp",
        "lng": "116.12454223632812",
        "lat": "24.334945678710938",
        "env": "{\"newTicket\":\"%s\",\"longitude\":\"116.12454223632812\",\"latitude\":\"24.334945678710938\",\"xAxes\":\"\",\"yAxes\":\"\",\"dchn\":\"Ep9b0kx\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x1800103b) NetType/WIFI Language/zh_CN miniProgram\",\"fromChannel\":\"2\",\"newAppid\":\"30012\",\"openId\":\"oJJUI0cENbOL64BDlWClGcr3OrIc\",\"openIdType\":\"1\",\"isHitButton\":false,\"isOpenWeb\":true,\"timeCost\":2882}" % token
    }
    json_str = json.dumps(data)
    response = requests.post(url=url, headers=heards, verify=False, data=json_str)
    msg(response.text)
    data = json.loads(response.text)

    errmsg = data['errmsg']
    if errmsg == 'success':
        msg('访问成功！')
    else:
        msg('访问失败！')




# 开启抽奖游戏➕抽奖
def manghe_kaiqi(token, xpsid, wsgsig):
    try:
        id = wsgsig[random.randint(0, 25)]
        url = f'https://ut.xiaojukeji.com/ut/welfare/api/blindBox/index?wsgsig={id}'
        heards = {
            "user-agent": 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
            "D-Header-T": f"{token}",
            "Content-Type": "application/json",
            'Host':'ut.xiaojukeji.com',
            'Origin': 'https://fine.udache.com',
             'Accept': 'application/json,text/plain,*/*',
             'Accept-Encoding': 'gzip,deflate,br',
            'Referer': 'https://fine.udache.com/',
            'Connection': 'keep-alive',
        }
        data = {
            "xbiz": "240400",
            "prod_key": "vendor",
            "xpsid": f"{xpsid}",
            "dchn": "Ep9b0kx",
            "xoid": "5781c9a1-f3ca-4c29-9e7b-e95df2397dab",
            "uid": "283726966498823",
            "xenv": "passenger",
            "xpsid_root": "2679b899c5634c8b902ddbf448d5dba3",
            "assist_check": True,
            "newCycle": True,
            "token": f"{token}",
            "platform": "na",
            "lng": "116.12454223632812",
            "lat": "24.334945678710938",
            "env": "{\"newTicket\":\"%s\",\"longitude\":\"116.12454223632812\",\"latitude\":\"24.334945678710938\",\"xAxes\":\"\",\"yAxes\":\"\",\"dchn\":\"Ep9b0kx\",\"userAgent\":\"User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0\",\"fromChannel\":\"2\",\"newAppid\":\"30012\",\"openId\":\"oJJUI0cENbOL64BDlWClGcr3OrIc\",\"openIdType\":\"1\",\"isHitButton\":false,\"isOpenWeb\":true,\"timeCost\":15845,\"xAxes\":\"\",\"yAxes\":\"\",\"dchn\":\"nr1on9k\",\"cityId\":\"156\",\"appVersion\":\"6.2.4\",\"wifi\":\"1\",\"model\":\"iPhone XR\",\"ddfp\":\"675688ccfd4560ccf3456e3b80156f06cda68424\",\"fromChannel\":\"1\"}" % token
        }
        json_str = json.dumps(data)
        response = requests.post(url=url, headers=heards, verify=False, data=json_str)
        person_json = json.loads(response.text)
        group_id = person_json['data']['blind_box']['group_info']['group_id']
        print(group_id)
        for _ in range(10):
            url = f'https://ut.xiaojukeji.com/ut/welfare/api/blindBox/flip?wsgsig={id}'
            heards = {
                "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x1800103b) NetType/WIFI Language/zh_CN miniProgram',
                "D-Header-T": f"{token}",
                "Content-Type": "application/json",
            }
            data = {
                "xbiz": "240400",
                "prod_key": "vendor",
                "xpsid": f"{xpsid}",
                "dchn": "Ep9b0kx",
                "xoid": "5781c9a1-f3ca-4c29-9e7b-e95df2397dab",
                "uid": "283726966498823",
                "xenv": "passenger",
                "xpsid_root": "2679b899c5634c8b902ddbf448d5dba3",
                "xpsid_from": "",
                "group_id": group_id,
                "sequence_id": random.randint(0, 100),
                "token": f"{token}",
                "platform": "na",
                "lng": "116.12454223632812",
                "lat": "24.334945678710938",
                "env": "{\"newTicket\":\"%s\",\"longitude\":\"116.12454223632812\",\"latitude\":\"24.334945678710938\",\"xAxes\":\"\",\"yAxes\":\"\",\"dchn\":\"Ep9b0kx\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x1800103b) NetType/WIFI Language/zh_CN miniProgram\",\"fromChannel\":\"2\",\"newAppid\":\"30012\",\"openId\":\"oJJUI0cENbOL64BDlWClGcr3OrIc\",\"openIdType\":\"1\",\"isHitButton\":false,\"isOpenWeb\":true}" % token
            }
            json_str = json.dumps(data)
            response = requests.post(url=url, headers=heards, verify=False, data=json_str)
            msg(response.text)
            data = json.loads(response.text)
            time.sleep(4)
            if data ['errmsg'] == '当前场次已结束，可以继续参加下一场' or data ['errmsg'] == '无可用机会':
                return
    except:
        msg('开启下一场失败！账号异常')



def main():
    msg(f'====================共{len(token_re)}滴滴盲盒个账号Cookie=========\n')
    for e, token in enumerate(token_re):
        msg(f'******开始【账号 {e + 1}】  *********\n')
        xpsid = get_xpsid()
        manghe_fangwen(token, xpsid, wsgsig)
        time.sleep(4)
        manghe_liulan(token,xpsid)
        time.sleep(4)
        manghe_kaiqi(token, xpsid, wsgsig)

        msg('\n')
    if run_send == 'yes':
        send('滴滴盲盒')  # 通知服务


if __name__ == '__main__':
    main()
