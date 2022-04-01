# -*- coding: utf-8 -*-
import json
import requests
import time
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
import logging

#根据抓包信息修改以下变量的值，这些变量用于构建请求头
cookie = "你抓到的安卓包中,druidv6.if.qidian.com/argus/api/v2/下的包的cookie"
catch_QDsign = "你抓到的安卓包中,druidv6.if.qidian.com/argus/api/v2/下的包的QDsign"

############ 解决计算QDSign需要的参数 #######
def handle():
    global catch_QDsign
    data = base64.b64decode(catch_QDsign)
    cryptor = DES3.new(key, DES3.MODE_CBC, b'01234567')
    msg = str(cryptor.decrypt(data))
    global list
    list=msg.split("|")
#########################################

############# 解决QDSign ##############
key = b'{1dYgqE)h9,R)hKqEcv4]k[h'

def calc_qdsign():
    #从其他请求的QDsign中获取计算签到请求的QDsign需要的值
    global list
    str=list[2]
    did=list[3]
    version=list[5]
    ts=getstamp()

    data = f'Rv1rPTnczce|{ts}|{str}|{did}|1|{version}|1|66cbf4b006fdedd1712e3a3bb1f861fb|f189adc92b816b3e9da29ea304d4a7e4'.encode()
    data = pad(data, 8)
    cryptor = DES3.new(key, DES3.MODE_CBC, b'01234567')
    data2 = cryptor.encrypt(data)
    qdsign = base64.b64encode(data2)
    return qdsign
#######################################

#创建一个字典对象，用于构建请求头
headers = {}

# 设置logging对象
logging.basicConfig(filename='./起点app自动签到日志.log',format='[%(filename)s-%(levelname)s:%(message)s]', level = logging.INFO,filemode='a',datefmt='%I:%M:%S %p')
 
def main_handler():
    # 设置请求头
    buildHearders()
    # 签到
    signResult = sign()

# 显示日期
def getTime():
    year = time.strftime("%Y", time.localtime())
    month = time.strftime("%m", time.localtime())
    day = time.strftime("%d", time.localtime())
    logging.info("{}年{}月{}日".format(year,month,day))

#获取时间戳
def getstamp():
    now = time.time()
    return int(round(now * 1000))

# 构建请求头
def buildHearders():
    headers["Cookie"] = cookie
    headers["QDSign"] = calc_qdsign()

# 签到
def sign():
    #指定url
    signUrl = "https://druidv6.if.qidian.com/argus/api/v2/checkin/checkin"
    result = requests.request("POST", signUrl, headers=headers,params="sessionKey=&banId=0&captchaTicket=&captchaRandStr=&challenge=&validate=&seccode=")

    # 显示日期
    getTime()
 
    #将发送签到后得到的响应信息取出并从json格式转回字典
    # print(result.content.decode("utf-8"))
    logging.info(result.content.decode("utf-8"))
    return json.loads(result.content)

# 用死循环实现定时任务
if __name__ == "__main__": 
    #一开始预处理
    handle()
    main_handler()
    #死循环实现定时任务
    while True:
        now_localtime = time.strftime("%H:%M", time.localtime())
        time.sleep(10)
        if now_localtime == "00:00":
            main_handler()
            time.sleep(61)