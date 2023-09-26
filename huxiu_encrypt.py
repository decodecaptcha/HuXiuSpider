# -*- coding: utf-8 -*-
# @Author : 艾登科技
# @Email : aidencaptcha@gmail.com
# @Address : https://github.com/aidencaptcha

import execjs
# 安装 python 第三方依赖
# pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

with open("huxiu_encrypt.js", "r") as f:
    source = f.read()
# print(source)

def username_encrypt(t):
    # 创建一个JavaScript环境
    ctx = execjs.compile(source)

    # 在JavaScript环境中执行函数
    result = ctx.call("get_username", t)

    # print("Result:", result)  # 输出: Result: 8
    return result