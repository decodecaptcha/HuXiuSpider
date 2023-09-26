# -*- coding: utf-8 -*-
# @Author : 艾登科技
# @Email : aidencaptcha@gmail.com
# @Address : https://github.com/aidencaptcha

# # HuXiuSpider

# GeetestCaptchaBreak 虎嗅网登录案例

# api 地址

# * [GeetestCaptchaBreak](https://github.com/aidencaptcha/GeetestCaptchaBreak)

# 有需求请在邮箱联系

# aidencaptcha@gmail.com

# TODO: 名词解释/字段说明
# captcha_id
# 验证公钥。32位字符串, 验证码的唯一标识, 对公众可见, 用以区分不同页面的验证模块。ID在极验后台创建获得, 请在每个验证场景部署不同的验证ID。
# 这里以虎嗅网登录/注册案例为案例, 地址 https://www.huxiu.com/
# captcha_id = "1879c3fbe17ecb87e1ccdc8e04b0602b", # 虎嗅网

# token
# 付费用户获取艾登科技的授权token
#  "token": "eyJ0********************UkE",

# proxy
# 代理格式说明:
# "https://ip:port", http 代理 无密码
# "https://user:pass@ip:port", http 代理 有密码
# "https://www.xxx.com:port"}, 隧道代理
# "socks5://user:pass@ip:port"}, socks 代理 有密码
# 总结: 只要是 requests, scrapy 请求库支持的代理格式都可以
# proxy = "http://127.0.0.1:8888"


import json
import random
from urllib.parse import urlencode
import requests
from loguru import logger
from huxiu_encrypt import username_encrypt

# 安装 python 第三方依赖
# pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/


logger.debug(r"""
    _     _      _                ____                _          _
   / \   (_)  __| |  ___  _ __   / ___|  __ _  _ __  | |_   ___ | |__    __ _ 
  / _ \  | | / _` | / _ \| '_ \ | |     / _` || '_ \ | __| / __|| '_ \  / _` |
 / ___ \ | || (_| ||  __/| | | || |___ | (_| || |_) || |_ | (__ | | | || (_| |
/_/   \_\|_| \__,_| \___||_| |_| \____| \__,_|| .__/  \__| \___||_| |_| \__,_|
                                              |_|
@Author : 艾登科技
@Email : aidencaptcha@gmail.com
@Address : https://github.com/aidencaptcha
@Description : API需求请在邮箱联系 aidencaptcha@gmail.com
""")


def huxiu(captcha_id, proxy, token):
    """ GeetestCaptchaBreak 虎嗅网登录案例 """
    # 请求1, 艾登科技的 API
    api_url = "http://42.194.245.28:8001/gtcap_api"
    headers = {
        "Connection": "close",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "captcha_id": captcha_id,
        "proxy": proxy,
        "token": token
    })
    response = requests.request("POST", api_url, data=data, headers=headers, timeout=30)
    assert response.text, "response.text is empty"
    res_json = json.loads(response.text)
    # logger.debug(res_json)

    # 解析 API 响应
    if res_json["succ"] == 1:
        # result 如果是空字符串"", 代表是第一次任务推入队列操作
        if res_json["result"] == "":
            logger.debug(f'任务已推入队列, 等待被消费, 当前请求次数量: {res_json["count"]}, 当前队列积压数量: {res_json["reply"]}')
            return

        data = res_json["result"]["data"]
        # 没有出现字符串 "captcha_output" 统一当异常不处理既可
        if "captcha_output" not in str(data):
            return

        # 提取令牌
        data = res_json["result"]["data"]
        proxy = res_json["result"]["proxy"]
        user_agent = res_json["result"]["user_agent"]
        lot_number = data["lot_number"]
        pass_token = data["pass_token"]
        gen_time = data["gen_time"]
        captcha_output = data["captcha_output"]

        # 请求 2 -- 虎嗅前端业务请求 发送短信验证码
        # 根据获取到的令牌, 进行前端业务请求--比如: 发送短信验证码
        loginCaptcha_url = "https://api-account.huxiu.com/v2/login/loginCaptcha"
        headers = {
            'authority': 'api-account.huxiu.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua-mobile': '?1',
            'user-agent': user_agent,
            'sec-ch-ua-platform': '"Android"',
            'origin': 'https://www.huxiu.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.huxiu.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'Hm_lvt_502e601588875750790bbe57346e972b=1695686357; Hm_lpvt_502e601588875750790bbe57346e972b=1695686357; huxiu_analyzer_wcy_id=304od7cm6p8wi2e37qy'
        }
        payload_dict = {
            "username": f"1772440{random.randint(1000, 9999)}", # 随机生成用户名/手机号
            "country": "+86",
            "captcha_id": captcha_id,
            "lot_number": lot_number,
            "pass_token": pass_token,
            "gen_time": gen_time,
            "captcha_output": captcha_output,
            "platform": "www"
        }
        # 加密前
        # logger.debug(f"loginCaptcha payload_dict: {payload_dict}")
        # 用户名/手机号加密
        payload_dict = username_encrypt(payload_dict)
        # 加密后
        # logger.debug(f"loginCaptcha payload_dict: {payload_dict}")
        # logger.debug(f"loginCaptcha payload_dict: {payload_dict}")
        payload_str = urlencode(payload_dict)
        # logger.debug(f"loginCaptcha payload_str: {payload_str}")
        response = requests.request("POST", loginCaptcha_url, headers=headers, data=payload_str, proxies={"all": proxy}, verify=False)
        return payload_dict["username"], response.text
        # 常见的响应:
        # {'success': True, 'data': {'message': '验证码发送成功'}, 'message': '请求成功'}
        # {'success': False, 'error': {'message': '验证码已发送，请稍候再试', 'code': 1005}, 'message': '验证码已发送，请稍候再试'}

    else:
        logger.debug("请求失败, 请联系技术")
        return


if __name__ == '__main__':
    # TODO: 名词解释/字段说明
    # captcha_id
    # 验证公钥。32位字符串, 验证码的唯一标识, 对公众可见, 用以区分不同页面的验证模块。ID在极验后台创建获得, 请在每个验证场景部署不同的验证ID。
    # 这里以虎嗅网登录/注册案例为案例, 地址 https://www.huxiu.com/
    captcha_id = "1879c3fbe17ecb87e1ccdc8e04b0602b" # 虎嗅网

    # token
    # 付费用户获取艾登科技的授权token
    token = "eyJ0********************UkE"

    # proxy
    # 代理格式说明:
    # "https://ip:port", http 代理 无密码
    # "https://user:pass@ip:port", http 代理 有密码
    # "https://www.xxx.com:port"}, 隧道代理
    # "socks5://user:pass@ip:port"}, socks 代理 有密码
    # 总结: 只要是 requests, scrapy 请求库支持的代理格式都可以
    # proxy = "http://127.0.0.1:8888"
    proxy = "http://127.0.0.1:51731"
    # 启动
    count = 0
    for i in range(100):
        res = huxiu(captcha_id, proxy, token)
        if res:
            username, text = res
            logger.debug(f"虎嗅网 username: {username}, 请求响应: {json.loads(text)}, 请求次数: {i+1}")
            count += 1
        else:
            pass

        # 速度限制
        # import time
        # time.sleep(1)