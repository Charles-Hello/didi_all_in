# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/24 12:13
@Auth ： maomao
@File ：maomao_didi_check_token.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
'''
cron: 0 0-23/5 * * *
new Env('滴滴token监测');
'''



import re
import requests
import json
import os
import sys
requests.packages.urllib3.disable_warnings()





with open(r'/ql/config/djangolog/diditoken.txt', 'r') as f2:
    a = f2.read()

token_re = re.findall('\"(.*)\"',a)
# print(token_re)


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
        # print(data)

        if data['errmsg'] == '查不到用户' :
            print('账号已经失效，正在执行删除操作')
            with open('12test', 'r') as r:
                lines = r.readlines()
            with open('12test', 'w') as w:
                for l in lines:
                    if token not in l:
                        w.write(l)
            print('失效账号删除成功')
        else:
            user_info = data['data']['name']
            msg('村民'+user_info)
    except:
        print('账号已经废了，正在执行删除操作')
        with open('12test', 'r') as r:
            lines = r.readlines()
        with open('12test', 'w') as w:
            for l in lines:
                if token not in l:
                    w.write(l)
        print('失效账号删除成功')



def main():
    for token in token_re:
        userinfo(token)


main()