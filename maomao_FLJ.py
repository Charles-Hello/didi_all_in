# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/26 10:57
@Auth ： maomao
@File ：maomao_FLJ.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import requests
import re
import json
import sys
import os
import random
requests.packages.urllib3.disable_warnings()
import time
#!/bin/env python3
# -*- coding: utf-8 -*
'''
cron: 22 10,15 * * *
new Env('滴滴app福利金签到');
'''


run_send = 'yes'

'''———————————————————————pycharm环境——————————————————————————————'''

with open('12test', 'r') as f2:
    token = f2.read()

'''———————————————————————pycharm环境——————————————————————————————'''

'''———————————————————————ql环境——————————————————————————————'''
# 
# with open(r'/ql/config/djangolog/diditoken.txt', 'r') as f2:
#     token = f2.read()


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



wsgsig=['dd03-vx9tq2onDp0IZqcYVoABxTjsa%2BXNwlstUQ6fOSmVa%2BX%2BZhfRmNkDw6zkAz0%2BZA8rsJ2%2BzMKjCoJLpecxVoEAOMK%2FBzf2SAJmXo6ax6Nre%2BnNYVNkX72aP6KjAJE',
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



#获取xpsid
def get_xpsid():
    try:
        url = f'https://v.didi.cn/DpQ3dga?appid=10000&lang=zh-CN&clientType=1&trip_cityid=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&channel=102&appversion=6.2.4&trip_country=CN&TripCountry=CN&lng=113.812212&maptype=soso&os=iOS&utc_offset=480&location_cityid=21&access_key_id=1&deviceid=99d8f16bacaef4eef6c151bcdfa095f0&cityid=21&location_country=CN&phone=UCvMSok42+5+tfafkxMn+A==&model=iPhone11&lat=23.016388&origin_id=1&client_type=1&terminal_id=1&sig=b84826e0429da615f74ec92157c513fa809e9e8b'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head (url=url, headers=heards, verify=False)    #获取响应请求头
        res = response.headers['Location']                                  #获取响应请求头
        # print(res)
        r = re.compile (r'root_xpsid=(.*?)&appid', re.M | re.S | re.I)
        xpsid = r.findall (res)
        xpsid = xpsid[0]
        print(xpsid)
        return xpsid
    except Exception as e:
        print(e)
        msg("获取xpsid失败，可能是表达式错误")


#查看福利金
def get_fulijin(token,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0, 25)]
        info_url = f'https://rewards.xiaojukeji.com/loyalty_credit/bonus/getWelfareUsage4Wallet?wsgsig={wsgsig}&token={token}&city_id=21'
        info_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "origin": "https://page.udache.com",
            "accept-language": "zh-cn",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "host": "rewards.xiaojukeji.com",
        }
        response = requests.get (url=info_url, headers=info_headers, verify=False)
        result = response.json()
        print(result)
        balance = result['data']['balance']
        msg("{}福利金".format(balance))

    except Exception as e:
        print(e)
        msg ("获取福利金信息失败,可能是token过期")



#执行积分签到
def do_sign1(token,xpsid):
    try:
        do_sign_url = f'https://ut.xiaojukeji.com/ut/welfare/api/action/dailySign'
        data = '{'+ r'"xbiz":"","prod_key":"welfare-center","xpsid":"' + f"{xpsid}" + r'","dchn":"62wjxq8","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r',","xpsid_from":"","xpsid_share":"","token":"' + f"{token}" + r'","lat":"23.016329481336804","lng":"113.81252766927084","platform":"na",'+ r'"env":"{\"cityId\":\"158\",\"token\":\"' + f'{token}' + r'\",\"longitude\":\"113.81252766927084\",\"latitude\":\"23.016329481336804\",\"appid\":\"30004\",\"fromChannel\":\"1\",\"deviceId\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"ddfp\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"appVersion\":\"6.2.4\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0\"}"}'


        do_sign_heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "origin": "https://page.udache.com",
            "accept-language": "zh-cn",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded",
            "host":"ut.xiaojukeji.com",
        }
        response = requests.post(url=do_sign_url,data=data,headers=do_sign_heards,verify=False)
        do_sign_ = response.json()
        print(do_sign_)
        code = do_sign_['errno']   #本次签到获得的积分
        if code == 40009:
            msg("今日福利金已签到，无需重复签到")
        elif code == 0:
            #prize_status = do_sign_['data']['prize_status']   #5天签到周期内签到第几天
            subsidy_amount = do_sign_['data']['subsidy_state']['subsidy_amount']
            msg("今日签到成功，获得福利金{}，".format(subsidy_amount))



    except Exception as e:
        print(e)
        msg ('滴滴福利金签到异常，可能是token过期')


def do_sign2(token,xpsid):
    try:
        url = f'https://bosp-api.xiaojukeji.com/gulfstream/hubble/open/signin/submit?wsgsig={token}'
        data = r'{"xbiz":"240200","prod_key":"custom","xpsid":"' + f"{xpsid}" + r',","dchn":"zjO1EbA","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r',","xpsid_from":"","xpsid_share":"","token":' + '"'+ f'{token}'+ '"'+ r',"lat":"23.01633056640625","lng":"113.8125230577257","city_id":158,"env":"{\"newTicket\":\"' + f'{token}' + r'\",\"latitude\":\"23.01633056640625\",\"longitude\":\"113.8125230577257\",\"cityId\":\"158\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0\",\"appVersion\":\"6.2.4\",\"wifi\":\"1\",\"model\":\"iPhone 11\",\"ddfp\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"fromChannel\":\"1\",\"newAppid\":\"10000\",\"isHitButton\":false,\"isOpenWeb\":true,\"timeCost\":31}","openid":"","platform":"na","res_params":"{\"resource_names\":\"pas_ut_discovery_banner1,pas_ut_discovery_billboard_card1,pas_ut_discovery_billboard_card2,pas_ut_discovery_billboard_card3,pas_ut_discovery_cx_resource_card,pas_ut_discovery_jifen_resource_card,pas_ut_discovery_banner2\",\"appversion\":\"6.2.4\",\"channel_id\":\"\",\"platform_type\":1}"}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "origin": "https://page.udache.com",
            "accept-language": "zh-cn",
            "accept": "application/json, text/plain, */*",
            "content-type":"application/json",
            "host":"bosp-api.xiaojukeji.com",
            "content-length":"1637",
        }
        response = requests.post(url=url,data=data,headers=headers,verify=False)
        do_sign_ = response.json()
        print(do_sign_)
        code = do_sign_['errno']   #本次签到获得的积分
        if code == 200100:
            msg("今日天天签到已签到，无需重复签到")
        elif code == 0:
            content = do_sign_['data']['content']
            content = content.replace('{icon}','')
            msg("今日天天签到签到成功，获得{}".format(content))
    except Exception as e:
        print(e)
        msg ('（滴滴天天签到异常，可能是token过期')
        # send ("滴滴天天签到", msg_info)

#参加瓜分
def guafen(token,xpsid,activity_id_tomorrow,task_id_tomorrow,count):
    try:
        url = f'https://ut.xiaojukeji.com/ut/welfare/api/action/joinDivide'
        data = r'{"xbiz":"","prod_key":"welfare-center","xpsid":"' + f"{xpsid}" + r'","dchn":"DpQ3dga","xoid":"9c52fa1a-ec11-46f9-9682-5d90694dd281","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r'","xpsid_from":"","xpsid_share":"","token":"' + f'{token}'+ '"'+ r',"lat":"23.016388346354166","lng":"113.81221218532986","platform":"na","env":"{\"cityId\":\"21\",\"token\":\"' + f'{token}' + r'\",\"longitude\":\"113.81221218532986\",\"latitude\":\"23.016388346354166\",\"appid\":\"30004\",\"fromChannel\":\"1\",\"deviceId\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"ddfp\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"appVersion\":\"6.2.4\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 BottomBar/on OffMode/0\"}","activity_id":' + f"{activity_id_tomorrow}" + r',"count":' + f"{count}" + r',"type":"ut_bonus"}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "origin": "https://page.udache.com",
            "host":"ut.xiaojukeji.com",
        }
        response = requests.post(url=url,data=data,headers=headers,verify=False)
        result = response.json()
        print(result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg("参加明日打卡瓜分活动成功")
        elif "活动已经被领取" in errmsg:
            msg("已参加打卡瓜分活动，请明天记得签到瓜分")
        else:
            print("打卡瓜分福利金活动未开启")

    except Exception as e:
        print(e)
        msg ('参加打卡瓜分异常，可能是token过期')

#签到瓜分
def guafen_Sign(token,xpsid,activity_id_today,task_id_today):
    try:
        url = f'https://ut.xiaojukeji.com/ut/welfare/api/action/divideReward'
        data = r'{"xbiz":"","prod_key":"welfare-center","xpsid":"' + f"{xpsid}" + r'","dchn":"DpQ3dga","xoid":"3b5d5c47-2c82-4914-b633-227dfc0c687a","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r'","xpsid_from":"","xpsid_share":"","token":"' + f'{token}' + r'","lat":"23.016388346354166","lng":"113.81221218532986","platform":"na","env":"{\"cityId\":\"21\",\"token\":\"' + f'{token}' + r'\",\"longitude\":\"113.81221218532986\",\"latitude\":\"23.016388346354166\",\"appid\":\"30004\",\"fromChannel\":\"1\",\"deviceId\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"ddfp\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"appVersion\":\"6.2.4\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 BottomBar/on OffMode/0\"}","activity_id":' + f"{activity_id_today}" + r',"task_id":' + f"{task_id_today}" + r'}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "origin": "https://page.udache.com",
            "host":"ut.xiaojukeji.com",
        }
        response = requests.post(url=url,data=data,headers=headers,verify=False)
        result = response.json()
        print(result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg("今日参加打卡瓜分活动成功")
        elif "活动已经被领取" in errmsg:
            msg("已参加打卡瓜分活动，请明天记得签到瓜分")
        else:
            print("打卡瓜分福利金活动未开启")

    except Exception as e:
        print(e)
        msg ('参加打卡瓜分签到，可能是token过期')

#获取瓜分活动ID
def guafen_id(token,xpsid):
    # try:
        url = f'https://ut.xiaojukeji.com/ut/welfare/api/home/init/v2'
        data = r'{"xbiz":"","prod_key":"welfare-center","xpsid":"' + f"{xpsid}" + r'","dchn":"DpQ3dga","xoid":"3b5d5c47-2c82-4914-b633-227dfc0c687a","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r'","xpsid_from":"","xpsid_share":"","token":"' + f'{token}' + r'","lat":"23.016388346354166","lng":"113.81221218532986","platform":"na","env":"{\"cityId\":\"21\",\"token\":\"' + f'{token}' + r'\",\"longitude\":\"113.81221218532986\",\"latitude\":\"23.016388346354166\",\"appid\":\"30004\",\"fromChannel\":\"1\",\"deviceId\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"ddfp\":\"99d8f16bacaef4eef6c151bcdfa095f0\",\"appVersion\":\"6.2.4\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 BottomBar/on OffMode/0\"}","resparams":"{\"resource_name\":\"ut_welfare_center_play_background,pas_ut_welfare_center_normal,pas_ut_welfare_center_abnormal,pas_ut_welfare_center_more\",\"height\":712,\"width\":534,\"city_id\":0,\"lat\":0,\"lng\":0,\"app_key\":\"server\",\"lang\":\"zh-CN\",\"token\":\"' + f'{token}' + r'\"}","assist_check":true,"os":"ios"}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "origin": "https://page.udache.com",
            "host":"ut.xiaojukeji.com",
        }
        response = requests.post(url=url,data=data,headers=headers,verify=False)
        result = response.json()
        print(result)
        # divide_data = result['data']['divide_data']['divide']
        # activity_id_today = divide_data['today']['activity_id']
        # task_id_today = divide_data[today]['task_id']
        # activity_id_tomorrow = divide_data['tomorrow']['activity_id']
        # task_id_tomorrow = divide_data['tomorrow']['task_id']
        # count = divide_data['tomorrow']['button']['count']
        # return activity_id_today,task_id_today,activity_id_tomorrow,task_id_tomorrow,count
    # except Exception as e:
    #     print(e)
    #     msg ('无法参加瓜分活动，请自行打开App查看是否有瓜分活动')
    #     return 0,0,0,0,0




def main():
    msg(f'====================共{len(token_re)}滴滴盲盒个账号Cookie=========\n')
    for e, token in enumerate(token_re):
        msg(f'******开始【账号 {e + 1}】  *********\n')
        xpsid = get_xpsid()
        do_sign1(token, xpsid)
        get_fulijin(token, wsgsig)
        do_sign2(token,xpsid)
        
        
        
        # guafen_id(token,xpsid)
        #
        #
        # activity_id_today, task_id_today, activity_id_tomorrow, task_id_tomorrow, count = guafen_id(token,xpsid)
        #
        # guafen_Sign(token,xpsid,activity_id_today,task_id_today)
        # guafen(token,xpsid,activity_id_tomorrow,task_id_tomorrow,count)



        msg('\n')
    if run_send == 'yes':
        send('滴滴盲盒')  # 通知服务


if __name__ == '__main__':
    main()
