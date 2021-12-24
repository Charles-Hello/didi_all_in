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
cron: 0 0-23/1 * * *
new Env('滴滴水果一条龙');
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

# with open(r'/ql/config/djangolog/diditoken.txt', 'r') as f1:
#     token = f1.read()


# pycharm目录
with open(r'滴滴token.txt', 'r') as f1:
    token = f1.read()


# 读取所有的token 给到tokenpro

token_re = re.findall('\"(.*)\"',token)


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


def userinfo(token):
    try:
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://fine.diditaxi.com.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
        }
        data = '{"xbiz":"240301","prod_key":"didi-orchard","dchn":"O9aM923","xenv":"passenger","xspm_from":"","xpsid_from":"","xpsid_share":"","platform":1,"token":"%s"}' % token

        response = requests.post(f'https://game.xiaojukeji.com/api/game/plant/get/address',
                                 headers=headers, data=data, verify=False)
        data = json.loads(response.text)
        user_info = data['data']['name']
        global a
        a = '村民👨 :' + user_info
        msg(a)
        return a
    except:
        a = '狗贼,这个叼毛还没有写收货地址'
        msg(a)
        msg('这个叼毛还没有写收货地址！请填写脚本再运行此通知')
        return a


def game(activity, token):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://fine.diditaxi.com.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
    }

    data = '{"xbiz":"240301","prod_key":"didi-orchard","dchn":"O9aM923","xenv":"passenger","xspm_from":"","xpsid_from":"","xpsid_share":"","platform":1,"token":"%s"}' % token

    response = requests.post(f'https://game.xiaojukeji.com/api/game/plant/{activity}'.format(activity=activity),
                             headers=headers, data=data, verify=False)

    data = json.loads(response.text)
    if activity == 'recBucketWater':
        try:
            coollect_water = data['data']['rec_water']
            msg('当前收集水滴💧：' + str(coollect_water))
        except:
            msg('当前水井情况💧：' + data['errmsg'])
    elif activity == 'receivePer':
        msg('正在收集化肥🍜ing.....')

    elif activity == 'watering':
        try:
            ripe = data['data']['tree_progress']
            remainder_water = data['data']['pack_water']

            # 这里我们除以30，执行浇三分之一的水
            num_water = str(round(int(remainder_water) / 30))
            msg('当前可浇水次数:' + str(round(int(remainder_water) / 10)) + '次')
            if int(str(round(int(remainder_water) / 10))) > 1:
                msg('正在执行浇水' + num_water + '次' + '\n或许会较长时间等待⌛️')
                num = 1
                for _ in range(round(int(remainder_water) / 30)):
                    headers = {
                        'Content-Type': 'application/json;charset=utf-8',
                        'Origin': 'https://fine.diditaxi.com.cn',
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
                    }
                    data_water = '{"xbiz":"240301","prod_key":"didi-orchard","dchn":"O9aM923","xenv":"passenger","xspm_from":"","xpsid_from":"","xpsid_share":"","platform":1,"token":"%s"}' % token

                    requests.post(
                        f'https://game.xiaojukeji.com/api/game/plant/watering',
                        headers=headers, data=data_water, verify=False)
                    # msg('正在执行第' + str(num) + '次浇水')
                    num = num + 1

            msg('结束浇水～辛苦你了💦')
            if data['data']['errmsg'] == '请先种一棵树吧' is True:
                msg(a + '的水果成熟啦🎉！')
            else:
                msg('当前水果🍉收成进度：' + ripe + "%")
        except:
            msg('当前账户水滴💧：' + data['errmsg'])

    elif activity == 'sign':
        if data['errmsg'] == 'success':
            msg('你已经签到成功了！')
        else:
            msg('叼毛，今天已经签到了！')


    elif activity == 'recExtWater':
        # msg(data)
        if data['errmsg'] == 'success':
            msg('收取水滴成功')
        else:
            msg('过段时间再来！')

    elif activity == 'recCommonBox':
        # msg(data)
        if data['errmsg'] == 'success':
            msg('收取宝箱宝物成功')
        else:
            msg('过段时间再来！')


    elif activity == 'heartbeatDog':
        # msg(data)
        if data['errmsg'] == 'success':
            msg('施肥料成功')
        else:
            msg('过段时间再来！')


# def fertilizer(token):
#     headers = {
#         'Content-Type': 'application/json;charset=utf-8',
#         'Origin': 'https://fine.diditaxi.com.cn',
#         'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
#     }
#     params = (
#         ('wsgsig',
#          'dd03-jms/j+O+nKsYgZmVoebaTKl3VRCzbSzySrpFvu/6VRCygOKmyFG9pKZLk4syg2CwQBR5S4TMl3pxBLNqoVjGpyxel4fXfIbxpljFvRO8r7yvf5GVuqW9vRw1loS'),
#     )
#     data = '{"count":1,"xbiz":"240301","prod_key":"didi-orchard","xpsid":"ffe8b988a2b347fa97560c751a7c51fd","dchn":"O9aM923","xoid":"S+cxEr+gQ862EyEv3cBWjQ","uid":"299067547479785","xenv":"passenger","xspm_from":"","xpsid_root":"ffe8b988a2b347fa97560c751a7c51fd","xpsid_from":"","xpsid_share":"","platform":1,"token":"%s"}' % token
#
#     response = requests.post('https://game.xiaojukeji.com/api/game/plant/fertilizer', headers=headers, params=params,
#                              data=data, verify=False)
#     data = json.loads(response.text)
#
#     if data['errmsg'] == 'success':
#         msg('领取施肥🍜成功！！')
#     else:
#         msg('恭喜你，领取了个屁！！')


'''
季度一次
dailyBox
"box_id":1,
"box_id":2,'''


def dailyBox(token):
    list = ['1', '2']
    for num in list:
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://fine.diditaxi.com.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
        }

        params = (
            ('wsgsig',
             'dd03-4LlttemucpqKykRVF8PAzavpB+ALvrsyE4YfRqoOB+AMyVfmfzaDzaXZ9zqMyd8wCvw+wBjvaoTNOBcqb+wazrcY9zq+QEpuG8kezknxbQh8RrDxGzVBxBbpau/'),
        )
        data = '{"box_id":%s,"xbiz":"240301","prod_key":"didi-orchard","xpsid":"ffe8b988a2b347fa97560c751a7c51fd","dchn":"O9aM923","xoid":"S+cxEr+gQ862EyEv3cBWjQ","uid":"299067547479785","xenv":"passenger","xspm_from":"","xpsid_root":"ffe8b988a2b347fa97560c751a7c51fd","xpsid_from":"","xpsid_share":"","platform":1,"token":"%s"}' % (
            num, token)

        response = requests.post('https://game.xiaojukeji.com/api/game/plant/dailyBox', headers=headers, params=params,
                                 data=data, verify=False)
        data = json.loads(response.text)
        if data['errmsg'] == 'success':
            msg('领取' + num + '季度💎奖励成功')
            break
        else:
            msg('领取' + num + '季度💎情况：恭喜你领取失败！！')


def get_award(token):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
            'Referer': 'https://fine.diditaxi.com.cn/',
        }

        params = (
            ('xenv', 'passenger'),
            ('game_id', '23'),
            ('loop', '1'),
            ('platform', '1'),
            ('token', token),
        )

        response = requests.get('https://game.xiaojukeji.com/api/game/mission/get', headers=headers, params=params,
                                verify=False)

        data_award = json.loads(response.text)

        for i in data_award['data']['missions']:
            headers = {
                'Content-Type': 'application/json;charset=utf-8',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',
            }

            params = (
                ('wsgsig',
                 'dd03-QT8Bv6u/z6WLY8jdnNpqWIRVTxGKxJu+lubkjOssTxGJYNN0X7vrX2RjwMWJYz0Mj3fTUIznwSRIoQKanNgXXSnmwTg7Zuf1ko8ZWLtiP6p8YpKLkogsjwmrPxO'),
            )

            data = '{{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"ffe8b988a2b347fa97560c751a7c51fd","dchn":"O9aM923","xoid":"S+cxEr+gQ862EyEv3cBWjQ","uid":"299067547479785","xenv":"passenger","xspm_from":"","xpsid_root":"ffe8b988a2b347fa97560c751a7c51fd","xpsid_from":"","xpsid_share":"","mission_id":{},"game_id":23,"platform":1,"token":"{}"}}'.format(
                i['id'], token)

            response = requests.post('https://game.xiaojukeji.com/api/game/mission/award', headers=headers,
                                     params=params,
                                     data=data, verify=False)
            # msg(response.text)
    except:
        pass


def xinshou(token):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0',

    }

    data = '{{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"46a5cbb12aed490989909317623ce214","dchn":"O9aM923","xoid":"VIdBMwzuSpa8IPNX9Y3Bzg","uid":"286475020565532","xenv":"passenger","xspm_from":"","xpsid_root":"46a5cbb12aed490989909317623ce214","xpsid_from":"","xpsid_share":"","selected":10,"platform":1,"token":"{}"}}'.format(
        token)

    response = requests.post('https://game.xiaojukeji.com/api/game/plant/newcomerSign', headers=headers,
                             data=data, verify=False)
    msg(response.text)


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
        # msg(xpsid)
        return xpsid
    except Exception as e:
        msg(e)
        msg("获取xpsid失败，可能是表达式错误")


# 获取小动物_id
def get_pet_id(token, xpsid, wsgsig):
    try:
        url = f'https://game.xiaojukeji.com/api/game/plant/enter?wsgsig={wsgsig}'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{token}",
            "Content-Type": "application/json",
        }
        data = '{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","assist_type":0,"encode_uid":"","is_old_player":true,"platform":1,"token":"' + f'{token}' + r'"}'
        response = requests.post(url=url, headers=heards, verify=False, data=data)
        result = response.json()
        # msg(result)
        pet_id = result['data']['lam_uid']
        return pet_id
    except:
        pass



# 访问公交车页面任务
def liulan_bus(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":256,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg(data)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("访问公交车页面任务已完成")
    else:
        msg("访问公交车页面任务早已完成，跳过执行环节")


# 访问成长会员任务
def liulan_chengzhang(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":258,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg(data)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("访问成长会员任务已完成")
    else:
        msg("访问成长会员任务早已完成，跳过执行环节")


# 固定入口进入游戏
def liuan_guding(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    nowtime = int(round(time.time() * 1000))
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":255,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg (result)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("固定入口进入游戏任务已完成")
    else:
        msg("固定入口进入游戏任务早已完成，跳过执行环节")


# 【浏览晒单区】任务
def liuan_shaidan(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":32,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg (result)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("浏览晒单区任务,任务已完成")
    else:
        msg("浏览晒单区任务,任务早已完成，跳过执行环节")


#浏览充值中心
def liulan_chongzhi(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":41,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg(data)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("访问充值中心已完成")
    else:
        msg("访问充值中心任务早已完成，跳过执行环节")







# 访问积分商城任务
def liulan_jifen(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":257,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg(data)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("访问积分商城任务已完成")
    else:
        msg("访问积分商城任务早已完成，跳过执行环节")


# 学会技能任务
def do_study(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":31,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)

    data = json.loads(response.text)
    # msg(data)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("学会技能任务已完成")
    else:
        msg("学会技能任务早已完成，跳过执行环节")


# 点击果园任务
def dianji_fruit(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":29,"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    data = json.loads(response.text)
    # msg(data)
    errmsg = data['errmsg']
    if errmsg == 'success':
        msg("点击果园任务任务已完成")
    elif "服务内部错误" in errmsg:
        msg("点击果园任务任务执行失败")
    else:
        msg("点击果园任务任务早已完成，跳过执行环节")


# 去除蚂蚱任务
def mazha(token, xpsid, wsgsig):
    for i in range(2):
        id = wsgsig[random.randint(0, 25)]
        url = f'https://game.xiaojukeji.com/api/game/plant/killWorm?wsgsig={id}'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","friend_id":null,"platform":1,"token":"' + f'{token}' + r'"}'
        response = requests.post(url=url, headers=heards, verify=False, data=data)
        data = json.loads(response.text)
        # msg(data)
        errmsg = data['errmsg']
        if errmsg == 'success':
            worm_num = data['data']['worm_num']
            if worm_num == 0:
                msg("去除蚂蚱任务已完成")
        elif "服务内部错误" in errmsg:
            msg("去除蚂蚱任务执行失败")
        else:
            msg("去除蚂蚱任务早已完成，跳过执行环节")


# 早起分享
def share(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]

    url = f'https://game.xiaojukeji.com/api/game/plant/shareEarlyBird?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    result = response.json()
    # msg(result)
    errmsg = result['errmsg']
    time.sleep(0.2)
    if errmsg == 'success':
        url = f'https://game.xiaojukeji.com/api/game/plant/recEarlyBird?wsgsig={wsgsig}'
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","is_fast":false,"water_status":0,"platform":1,"token":"' + f'{token}' + r'"}'
        response = requests.post(url=url, headers=heards, verify=False, data=data)
        result = response.json()
        # msg(result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg("早起分享任务执行成功，获得100g水滴")
        elif "对应奖励已领取" in errmsg:
            msg("早起分享早已完成，跳过执行环节")
        elif "请稍后再试" in errmsg:
            msg("早起分享异常，请重新执行")
        elif "当前条件还不满足" in errmsg:
            msg("早起分享异常，请在中午12点前执行一次脚本")
    elif "今天已经分享" in errmsg:
        msg("早起分享早已完成，跳过执行环节")
    else:
        msg("请在中午12点前查看手机APP上时候有早起鸟分享活动")


# 领取饭点水滴8-10,12-14，15-17
def fandian(token, xpsid, wsgsig):
    wsgsig = wsgsig[random.randint(0, 25)]
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f8')
    url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://fine.didialift.com/",
        "Host": "game.xiaojukeji.com",
        "Origin": "https://fine.didialift.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "D-Header-T": f"{token}",
        "Content-Type": "application/json",
    }
    if nowtime > get_time1 and nowtime < get_time2:
        fdsd_id = 251
    elif nowtime > get_time2 and nowtime < get_time3:
        fdsd_id = 252
    elif nowtime > get_time3 and nowtime < get_time4:
        fdsd_id = 253
    else:
        return 0
    data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":' + f"{fdsd_id}" + r',"game_id":23,"platform":1,"token":"' + f'{token}' + r'"}'
    response = requests.post(url=url, headers=heards, verify=False, data=data)
    result = response.json()
    # msg (result)
    errmsg = result['errmsg']
    if errmsg == 'success':
        msg("领取饭店水滴")
    else:
        msg("未到时间领取，饭点水滴，跳过执行环节")


# 使用肥料
def shifei(token, xpsid, wsgsig):
    for i in range(3):
        id = wsgsig[random.randint(0, 25)]
        nowtime = int(round(time.time() * 1000))
        url = f'https://game.xiaojukeji.com/api/game/plant/fertilizer?wsgsig={id}'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","count":1,"platform":1,"token":"' + f'{token}' + r'"}'
        response = requests.post(url=url, headers=heards, verify=False, data=data)
        result = response.json()
        # print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            tree_nutrient = result['data']['tree_nutrient']  # 当前肥力
            pack_fer = result['data']['pack_fer']
            msg('施肥成功！')
        else:
            pass










def main():
    msg(f'====================共{len(token_re)}滴滴快车🚗个账号Cookie=========\n')
    for e, token in enumerate(token_re):
        msg(f'******开始【账号 {e + 1}】 {userinfo(token)} *********\n')
        xpsid = get_xpsid()
        get_pet_id(token, xpsid, wsgsig)
        game('sign', token)  # 这个是登陆
        time.sleep(3)
        shifei(token, xpsid, wsgsig)  # 先施肥，后浇水!
        time.sleep(3)
        game('watering', token)  # 这个是浇水
        time.sleep(3)
        game('recBucketWater', token)  # 不定时收取水滴
        time.sleep(3)
        game('receivePer', token)  # 不定时收取化肥
        time.sleep(3)
        game('recExtWater', token)  # 不定时收取水滴
        time.sleep(3)
        game('recCommonBox', token)  # 不定时收取宝箱
        time.sleep(3)
        game('heartbeatDog', token)  # 不定时施肥化肥
        time.sleep(3)
        xinshou(token)
        time.sleep(3)
        dailyBox(token)
        time.sleep(3)
        fandian(token, xpsid, wsgsig)
        time.sleep(3)
        liulan_chongzhi(token, xpsid, wsgsig)
        time.sleep(3)
        liulan_chengzhang(token, xpsid, wsgsig)
        time.sleep(3)
        liulan_bus(token, xpsid, wsgsig)
        time.sleep(3)
        liuan_shaidan(token, xpsid, wsgsig)
        time.sleep(3)
        liuan_guding(token, xpsid, wsgsig)
        time.sleep(3)
        dianji_fruit(token, xpsid, wsgsig)
        time.sleep(3)
        do_study(token, xpsid, wsgsig)
        time.sleep(3)
        liulan_jifen(token, xpsid, wsgsig)
        time.sleep(3)
        share(token, xpsid, wsgsig)
        time.sleep(3)
        mazha(token, xpsid, wsgsig)
        time.sleep(3)
        get_award(token)
        msg('\n')
    if run_send == 'yes':
        send('滴滴快车🚗')  # 通知服务


if __name__ == '__main__':
    main()
