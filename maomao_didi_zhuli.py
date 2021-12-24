# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/24 12:54
@Auth ： maomao
@File ：maomao_didi_zhuli.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

'''
cron: 0 5 * * *
new Env('滴滴吸助力');
'''


'''
token是工具人的
'''
'''
ocrd_token是主人的
'''
import requests
import json
import re
import os
import sys
requests.packages.urllib3.disable_warnings()
run_send = 'yes'



'''———————————————————————pycharm环境——————————————————————————————'''


# with open('12test', 'r') as f2:
#     a = f2.read()
    
'''———————————————————————pycharm环境——————————————————————————————'''











'''———————————————————————ql环境——————————————————————————————'''

with open(r'/ql/config/djangolog/diditoken.txt', 'r') as f2:
    a = f2.read()
    
    
'''———————————————————————ql环境——————————————————————————————'''




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






token_re = re.findall('\"(.*)\"',a)


'''share_id和ocrd_token应该是变化的'''


share_id = "6c4fad2069b3823675653c140630c352"


ocrd_token = 'ocrd9s4RF4PhxKpNwNmtL0IcYIZHyEHM82MX9G37OEckjruqw1AMwP5Fswk-b9t_c2-bPpZTaOkU8u8lZNIkoY2pBGXRRRFmIpIwM1GaqguzEGk0z8NL725uwqyECrMRIPyd-CeylZG7917dLBfhShRhJTY-r-_7shJNVX0XbkTqVfM4HOFOkMxStzRqPV4eZ_ZJ6P4LAAD__w=='






def didi_zhuli(token, ocrd_token, share_id):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x1800103b) NetType/WIFI Language/zh_CN',

    }
    data = {
        "token": token,
        "lat": "24.332400987413195",
        "lng": "116.12941379123264",
        "env": "{\"token\":\"%s\"}" % ocrd_token,
        "resparams": "{\"token\":\"%s\"}" % ocrd_token,
        "share_id": share_id
    }
    json_str = json.dumps(data)
    response = requests.post('https://ut.xiaojukeji.com/ut/welfare/api/home/assist', headers=headers, data=json_str,
                             verify=False)
    # msg(response.text)

    data = json.loads(response.text)
    result = data['data']['toast']
    msg(result)



def main():
    for token in token_re:
        didi_zhuli(token, ocrd_token, share_id)
        
    if run_send == 'yes':
        send('滴滴快车🚗')  # 通知服务

main()
